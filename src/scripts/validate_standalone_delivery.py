#!/usr/bin/env python3
"""Strict acceptance gate for the only customer-facing PixelPerfect deliverable."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    import numpy as np
    from PIL import Image, ImageCms, ImageOps
    from skimage.metrics import structural_similarity
    import skimage
except ImportError as exc:  # pragma: no cover - surfaced as a clear CLI blocker
    raise SystemExit(
        "Missing image verification dependencies. Install requirements-dev.txt "
        "(Pillow, NumPy and scikit-image) before using the final delivery gate."
    ) from exc


class DeliveryValidationError(ValueError):
    """Raised when an HTML artifact is not eligible for final delivery."""


RESOURCE_ATTRIBUTES = {
    "img": {"src", "srcset"},
    "script": {"src"},
    "link": {"href"},
    "source": {"src", "srcset"},
    "video": {"src", "poster"},
    "audio": {"src"},
    "track": {"src"},
    "iframe": {"src"},
    "object": {"data"},
    "embed": {"src"},
    "input": {"src"},
}
CSS_URL = re.compile(r"url\(\s*(?:['\"]([^'\"]+)['\"]|([^)]*))\s*\)", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\s+(?:url\()?\s*['\"]?([^'\";)\s]+)", re.IGNORECASE)
HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
METRIC_ALGORITHM = "rgb-max-channel-mismatch+rgb-mae+ssim"
METRIC_ALGORITHM_VERSION = f"numpy-{np.__version__};scikit-image-{skimage.__version__};ssim-win7"


def _fail(message: str) -> None:
    raise DeliveryValidationError(message)


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        _fail(f"{label} is not valid UTF-8 JSON: {exc}")
    if not isinstance(value, dict):
        _fail(f"{label} must contain a JSON object")
    return value


def _check_sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or not HEX64.fullmatch(value):
        _fail(f"{label} must be a 64-character SHA-256 hex digest")


def _is_embedded_or_fragment(uri: str) -> bool:
    value = uri.strip().strip("\"'")
    return value.startswith(("data:", "#"))


class _HTMLInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.layer_ids: list[str] = []
        self.resource_refs: list[tuple[str, str, str]] = []
        self.css_chunks: list[str] = []
        self.in_style = False
        self.has_html = False
        self.has_head = False
        self.has_body = False
        self.has_artboard_marker = False
        self.artboard_dimensions: list[tuple[int, int]] = []
        self.script_chunks: list[str] = []
        self.in_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {key.lower(): (value or "") for key, value in attrs}
        if tag == "html": self.has_html = True
        if tag == "head": self.has_head = True
        if tag == "body": self.has_body = True
        if tag in {"main", "div", "section", "svg", "canvas"} and any(k in values for k in ("data-artboard", "data-canvas-width", "data-layer")):
            self.has_artboard_marker = True
            if "data-canvas-width" in values and "data-canvas-height" in values:
                try:
                    self.artboard_dimensions.append((int(values["data-canvas-width"]), int(values["data-canvas-height"])))
                except ValueError:
                    self.artboard_dimensions.append((-1, -1))
        layer_id = values.get("data-layer") or values.get("data-layer-id")
        if layer_id:
            self.layer_ids.append(layer_id)
        for attr in RESOURCE_ATTRIBUTES.get(tag, set()):
            uri = values.get(attr)
            if not uri:
                continue
            if attr == "srcset":
                # srcset is deliberately rejected unless every candidate is a data URI.
                # Parsing arbitrary data URI comma payloads is ambiguous, so require src instead.
                self.resource_refs.append((tag, attr, uri))
            else:
                self.resource_refs.append((tag, attr, uri))
        if tag == "style":
            self.in_style = True
        if tag == "script":
            self.in_script = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style":
            self.in_style = False
        if tag.lower() == "script":
            self.in_script = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.css_chunks.append(data)
        if self.in_script:
            self.script_chunks.append(data)


def _check_no_external_resources(html_text: str, inventory: _HTMLInventory) -> list[str]:
    external: list[str] = []
    for tag, attr, uri in inventory.resource_refs:
        if attr == "srcset":
            external.append(f"<{tag} {attr}> uses srcset; use embedded data URI src instead")
        elif not _is_embedded_or_fragment(uri):
            external.append(f"<{tag} {attr}={uri!r}> is not embedded")

    css_text = "\n".join(inventory.css_chunks)
    for match in CSS_URL.finditer(css_text):
        uri = (match.group(1) or match.group(2) or "").strip()
        if uri and not _is_embedded_or_fragment(uri):
            external.append(f"CSS url({uri!r}) is not embedded")
    for match in CSS_IMPORT.finditer(css_text):
        uri = match.group(1).strip()
        if not _is_embedded_or_fragment(uri):
            external.append(f"CSS @import {uri!r} is not embedded")
    # Also inspect inline style attributes, which HTMLParser exposes on start tags.
    for match in re.finditer(r"\bstyle\s*=\s*(['\"])(.*?)\1", html_text, re.IGNORECASE | re.DOTALL):
        inline_style = match.group(2)
        for url_match in CSS_URL.finditer(inline_style):
            uri = (url_match.group(1) or url_match.group(2) or "").strip()
            if uri and not _is_embedded_or_fragment(uri):
                external.append(f"inline CSS url({uri!r}) is not embedded")
    script_text = "\n".join(inventory.script_chunks)
    for pattern, label in (
        (r"\bfetch\s*\(", "fetch()"),
        (r"\bXMLHttpRequest\b", "XMLHttpRequest"),
        (r"\bWebSocket\s*\(", "WebSocket"),
        (r"\bEventSource\s*\(", "EventSource"),
        (r"\bimport\s*\(", "dynamic import()"),
    ):
        if re.search(pattern, script_text):
            external.append(f"inline JavaScript uses network-capable {label}; offline standalone gate cannot pass")
    return external


def _read_rgb(path: Path, alpha_background: tuple[int, int, int] | None) -> tuple[np.ndarray, str]:
    try:
        with Image.open(path) as opened:
            detected_format = opened.format or "UNKNOWN"
            image = ImageOps.exif_transpose(opened)
            icc = image.info.get("icc_profile")
            if icc:
                try:
                    source_profile = ImageCms.ImageCmsProfile(__import__("io").BytesIO(icc))
                    image = ImageCms.profileToProfile(image, source_profile, ImageCms.createProfile("sRGB"), outputMode="RGBA" if "A" in image.getbands() else "RGB")
                except Exception as exc:
                    _fail(f"Could not normalize embedded ICC profile in {path.name}: {exc}")
            if "A" in image.getbands():
                rgba = image.convert("RGBA")
                alpha = rgba.getchannel("A")
                if alpha.getextrema() != (255, 255):
                    if alpha_background is None:
                        _fail(f"{path.name} contains transparency but no comparison alpha_background_rgb is declared")
                    background = Image.new("RGBA", rgba.size, (*alpha_background, 255))
                    image = Image.alpha_composite(background, rgba).convert("RGB")
                else:
                    image = rgba.convert("RGB")
            else:
                image = image.convert("RGB")
            return np.asarray(image, dtype=np.uint8), detected_format
    except DeliveryValidationError:
        raise
    except Exception as exc:
        _fail(f"Could not decode comparison image {path}: {exc}")


def _calculate_metrics(reference_path: Path, rendered_path: Path, pixel_threshold_rgb: int, alpha_background: tuple[int, int, int] | None = None) -> dict[str, float]:
    reference, _ = _read_rgb(reference_path, alpha_background)
    rendered, _ = _read_rgb(rendered_path, alpha_background)
    if reference.shape != rendered.shape:
        _fail(f"Reference/render pixel arrays must match exactly; got {reference.shape} vs {rendered.shape}")
    difference = np.abs(reference.astype(np.int16) - rendered.astype(np.int16))
    mismatch_ratio = float(np.mean(np.max(difference, axis=2) > pixel_threshold_rgb))
    mae = float(np.mean(difference))
    ssim = float(structural_similarity(reference, rendered, channel_axis=2, data_range=255, win_size=7, gaussian_weights=False))
    return {"mismatch_ratio": mismatch_ratio, "mae": mae, "ssim": ssim}


def validate_delivery(html_path: Path | str, manifest_path: Path | str, qa_path: Path | str, reference_path: Path | str, rendered_path: Path | str) -> dict[str, Any]:
    html_file = Path(html_path).resolve(strict=True)
    manifest_file = Path(manifest_path).resolve(strict=True)
    qa_file = Path(qa_path).resolve(strict=True)
    reference_file = Path(reference_path).resolve(strict=True)
    rendered_file = Path(rendered_path).resolve(strict=True)
    if html_file.suffix.lower() != ".html":
        _fail("The sole user-facing deliverable must be an .html file")
    if html_file.stat().st_size == 0:
        _fail("Standalone HTML is empty")

    html_bytes = html_file.read_bytes()
    try:
        html_text = html_bytes.decode("utf-8")
    except UnicodeDecodeError:
        _fail("Standalone HTML must be UTF-8")
    lowered = html_text.lower()
    if "<!doctype html" not in lowered or "</html>" not in lowered:
        _fail("A complete HTML5 document is required")

    inventory = _HTMLInventory()
    try:
        inventory.feed(html_text)
        inventory.close()
    except Exception as exc:
        _fail(f"HTML parsing failed: {exc}")
    if not (inventory.has_html and inventory.has_head and inventory.has_body):
        _fail("HTML document must contain html, head and body elements")
    if not inventory.has_artboard_marker:
        _fail("HTML must expose an explicit artboard marker")

    external = _check_no_external_resources(html_text, inventory)
    if external:
        _fail("Standalone HTML has runtime dependencies: " + "; ".join(external))

    manifest = _load_json(manifest_file, "Layer manifest")
    canvas = manifest.get("canvas")
    layers = manifest.get("layers")
    if not isinstance(canvas, dict) or not isinstance(layers, list) or not layers:
        _fail("Layer manifest requires canvas dimensions and a non-empty layers array")
    if manifest.get("status") != "frozen":
        _fail("The approved layer manifest must be frozen before final delivery")
    width, height = canvas.get("width_px"), canvas.get("height_px")
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        _fail("Manifest canvas dimensions must be positive integers")
    if (width, height) not in inventory.artboard_dimensions:
        _fail("HTML data-canvas-width and data-canvas-height must exactly match the frozen manifest")
    manifest_ids = [layer.get("id") for layer in layers if isinstance(layer, dict)]
    if len(manifest_ids) != len(layers) or any(not isinstance(item, str) or not item for item in manifest_ids):
        _fail("Every manifest layer must have a non-empty string id")
    if len(manifest_ids) != len(set(manifest_ids)):
        _fail("Manifest layer IDs must be unique")
    source_record = manifest.get("source")
    if not isinstance(source_record, dict):
        _fail("Frozen layer manifest must include original source metadata")
    for field in ("filename", "detected_format", "sha256", "byte_size", "width_px", "height_px", "normalized_width_px", "normalized_height_px", "mode", "exif_orientation", "icc_profile_sha256", "exif_orientation_transform"):
        if field not in source_record:
            _fail(f"Manifest source.{field} is required")
    _check_sha(source_record.get("sha256"), "manifest source.sha256")
    if source_record.get("byte_size") != reference_file.stat().st_size:
        _fail("Manifest source.byte_size does not match the supplied reference file")
    if source_record.get("sha256") != hashlib.sha256(reference_file.read_bytes()).hexdigest():
        _fail("Manifest source.sha256 does not match the supplied original reference bytes")
    with Image.open(reference_file) as source_image:
        source_detected_format = source_image.format or "UNKNOWN"
        source_mode = source_image.mode
        raw_width, raw_height = source_image.size
        exif = source_image.getexif()
        exif_orientation = exif.get(274, 1)
        icc_profile = source_image.info.get("icc_profile")
        icc_sha256 = hashlib.sha256(icc_profile).hexdigest() if icc_profile else None
        normalized_width, normalized_height = ImageOps.exif_transpose(source_image).size
    if source_record.get("width_px") != raw_width or source_record.get("height_px") != raw_height:
        _fail("Manifest source raw dimensions do not match the supplied reference file")
    if source_record.get("normalized_width_px") != normalized_width or source_record.get("normalized_height_px") != normalized_height:
        _fail("Manifest source normalized dimensions do not match the EXIF-normalized reference")
    if (normalized_width, normalized_height) != (width, height):
        _fail("Manifest normalized source dimensions must match the frozen native artboard")
    if source_record.get("exif_orientation") != exif_orientation:
        _fail("Manifest source.exif_orientation does not match the source file metadata")
    if source_record.get("icc_profile_sha256") != icc_sha256:
        _fail("Manifest source.icc_profile_sha256 does not match the source file bytes")
    if source_record.get("detected_format") != source_detected_format:
        _fail("Manifest source.detected_format does not match the source file bytes")
    if source_record.get("mode") != source_mode:
        _fail("Manifest source.mode does not match the source file bytes")

    asset_records = manifest.get("assets", [])
    if not isinstance(asset_records, list):
        _fail("Manifest assets must be an array")
    asset_ids = set()
    for asset in asset_records:
        if not isinstance(asset, dict) or not isinstance(asset.get("asset_id"), str) or not asset["asset_id"]:
            _fail("Each manifest asset needs a stable asset_id")
        _check_sha(asset.get("sha256"), f"asset {asset.get('asset_id')} sha256")
        if asset["asset_id"] in asset_ids:
            _fail(f"Duplicate manifest asset_id: {asset['asset_id']}")
        asset_ids.add(asset["asset_id"])
    missing_assets = sorted({layer.get("asset_id") for layer in layers if layer.get("asset_id") not in (None, "")} - asset_ids)
    if missing_assets:
        _fail(f"Layer references missing manifest assets: {missing_assets}")
    embedded_asset_hashes = set()
    for match in re.finditer(r"data:[^,;\s]+(?:;[^,\s]+)*;base64,([A-Za-z0-9+/=\r\n]+)", html_text, re.IGNORECASE):
        try:
            embedded_asset_hashes.add(hashlib.sha256(base64.b64decode(match.group(1), validate=False)).hexdigest())
        except Exception:
            _fail("HTML contains a malformed base64 data URI")
    missing_embedded = sorted(asset["asset_id"] for asset in asset_records if asset["sha256"].lower() not in embedded_asset_hashes)
    if missing_embedded:
        _fail(f"Manifest assets are not embedded byte-for-byte in the standalone HTML: {missing_embedded}")
    if len(inventory.layer_ids) != len(set(inventory.layer_ids)):
        _fail("HTML data-layer IDs must be unique")
    if set(inventory.layer_ids) != set(manifest_ids):
        missing = sorted(set(manifest_ids) - set(inventory.layer_ids))
        extra = sorted(set(inventory.layer_ids) - set(manifest_ids))
        _fail(f"Manifest/HTML layer mismatch; missing in HTML={missing}, extra in HTML={extra}")

    qa = _load_json(qa_file, "QA report")
    if qa.get("status") != "PASS":
        _fail("QA status must be PASS; partial or exception states are not deliverable")
    reference, render = qa.get("reference"), qa.get("render")
    if not isinstance(reference, dict) or not isinstance(render, dict):
        _fail("QA report requires reference and render metadata")
    for label, record in (("reference", reference), ("render", render)):
        if record.get("width_px") != width or record.get("height_px") != height:
            _fail(f"QA {label} dimensions must exactly match the manifest artboard")
        _check_sha(record.get("sha256"), f"QA {label}.sha256")
    _check_sha(reference.get("sha256"), "QA reference.sha256")
    if not isinstance(reference.get("detected_format"), str) or not reference["detected_format"]:
        _fail("QA reference must record detected_format from file bytes")
    if not isinstance(render.get("detected_format"), str) or not render["detected_format"]:
        _fail("QA render must record detected_format from file bytes")
    if hashlib.sha256(reference_file.read_bytes()).hexdigest() != reference.get("sha256"):
        _fail("QA reference hash does not match the supplied original reference file")
    if hashlib.sha256(rendered_file.read_bytes()).hexdigest() != render.get("sha256"):
        _fail("QA render hash does not match the supplied final render capture")
    comparison = qa.get("comparison")
    if not isinstance(comparison, dict):
        _fail("QA comparison metrics are required")
    alpha_bg_raw = comparison.get("alpha_background_rgb")
    alpha_background = None
    if alpha_bg_raw is not None:
        if not isinstance(alpha_bg_raw, list) or len(alpha_bg_raw) != 3 or any(not isinstance(v, int) or not 0 <= v <= 255 for v in alpha_bg_raw):
            _fail("comparison.alpha_background_rgb must be three integer RGB channels")
        alpha_background = tuple(alpha_bg_raw)
    reference_pixels, reference_format = _read_rgb(reference_file, alpha_background)
    render_pixels, render_format = _read_rgb(rendered_file, alpha_background)
    if reference_pixels.shape[:2] != (height, width) or render_pixels.shape[:2] != (height, width):
        _fail("Decoded reference and render image dimensions must exactly match the frozen artboard")
    if reference.get("detected_format") and reference["detected_format"] != reference_format:
        _fail("QA reference detected_format does not match the source file bytes")
    if render.get("detected_format") and render["detected_format"] != render_format:
        _fail("QA render detected_format does not match the render file bytes")

    environment = qa.get("environment")
    if not isinstance(environment, dict) or not all(isinstance(environment.get(k), str) and environment[k].strip() for k in ("browser", "version")):
        _fail("QA environment must record browser name and exact version")
    if not isinstance(environment.get("device_scale_factor"), (int, float)) or environment["device_scale_factor"] <= 0:
        _fail("QA environment must record a positive device scale factor")

    if comparison.get("algorithm") != METRIC_ALGORITHM:
        _fail(f"QA comparison.algorithm must be {METRIC_ALGORITHM!r}")
    if comparison.get("algorithm_version") != METRIC_ALGORITHM_VERSION:
        _fail(f"QA comparison.algorithm_version must match the validator runtime: {METRIC_ALGORITHM_VERSION}")
    if not isinstance(comparison.get("preprocessing"), str) or not comparison["preprocessing"].strip():
        _fail("QA comparison.preprocessing is required")
    metric_values = {}
    for field in ("pixel_threshold_rgb", "mismatch_ratio", "mae", "ssim"):
        value = comparison.get(field)
        if not isinstance(value, (int, float)):
            _fail(f"QA comparison.{field} must be numeric")
        metric_values[field] = float(value)
    if not 0 <= metric_values["pixel_threshold_rgb"] <= 255 or int(metric_values["pixel_threshold_rgb"]) != metric_values["pixel_threshold_rgb"]:
        _fail("pixel_threshold_rgb must be an integer in [0,255]")
    if not 0 <= metric_values["mismatch_ratio"] <= 1 or not 0 <= metric_values["ssim"] <= 1 or metric_values["mae"] < 0:
        _fail("QA comparison metrics are outside valid ranges")
    measured = _calculate_metrics(reference_file, rendered_file, int(metric_values["pixel_threshold_rgb"]), alpha_background)
    for field in ("mismatch_ratio", "mae", "ssim"):
        if not math.isclose(metric_values[field], measured[field], rel_tol=0, abs_tol=1e-6):
            _fail(f"QA comparison.{field} does not match recomputed image measurement; reported={metric_values[field]}, measured={measured[field]}")

    thresholds = comparison.get("acceptance_thresholds")
    if not isinstance(thresholds, dict):
        _fail("An explicit numerical-threshold status is required")
    if not isinstance(thresholds.get("profile_id"), str) or not thresholds["profile_id"].strip():
        _fail("A named threshold profile or diagnostic-only label is required")

    required_passes = {"structural", "fidelity", "finishing"}
    passes = qa.get("passes")
    if not isinstance(passes, list) or set(passes) != required_passes:
        _fail("All three QA passes are mandatory exactly once: structural, fidelity and finishing")

    visual_review = qa.get("visual_review")
    if not isinstance(visual_review, dict):
        _fail("A direct visual_review record is required for final delivery")
    if visual_review.get("status") != "PASS" or visual_review.get("method") != "direct_visual_inspection":
        _fail("visual_review must record PASS from direct_visual_inspection")
    if not isinstance(visual_review.get("reviewer"), str) or not visual_review["reviewer"].strip():
        _fail("visual_review must identify the reviewing agent or person")
    if visual_review.get("reference_sha256") != reference.get("sha256"):
        _fail("visual_review reviewed reference hash does not match the QA reference hash")
    if visual_review.get("render_sha256") != render.get("sha256"):
        _fail("visual_review reviewed render hash does not match the QA render hash")
    review_passes = visual_review.get("passes")
    if not isinstance(review_passes, list) or set(review_passes) != required_passes:
        _fail("visual_review must bind all three review passes to the inspected reference/render pair")
    regions_reviewed = visual_review.get("critical_regions_reviewed")
    if not isinstance(regions_reviewed, list) or not regions_reviewed or any(not isinstance(item, str) or not item.strip() for item in regions_reviewed):
        _fail("visual_review must identify the critical regions inspected")

    calibration_status = thresholds.get("calibration_status")
    if calibration_status == "validated":
        if thresholds.get("source") not in {"user_approved", "calibrated_benchmark", "validated_profile"}:
            _fail("Validated acceptance threshold source must be user-approved or benchmark/profile validated")
        max_mismatch, max_mae, min_ssim = (thresholds.get("max_mismatch_ratio"), thresholds.get("max_mae"), thresholds.get("min_ssim"))
        if not all(isinstance(v, (int, float)) for v in (max_mismatch, max_mae, min_ssim)):
            _fail("Validated thresholds must define max_mismatch_ratio, max_mae and min_ssim")
        if not (0 <= max_mismatch <= 1 and max_mae >= 0 and 0 <= min_ssim <= 1):
            _fail("Acceptance threshold values are outside valid ranges")
        if metric_values["mismatch_ratio"] > max_mismatch or metric_values["mae"] > max_mae or metric_values["ssim"] < min_ssim:
            _fail("Measured visual metrics fall outside the calibrated acceptance profile")
        calibration_profile = thresholds["profile_id"]
    elif calibration_status == "diagnostic_only":
        if thresholds.get("source") != "diagnostic_only":
            _fail("diagnostic_only metrics must use source=diagnostic_only")
        calibration_profile = "diagnostic_only_visual_review"
    else:
        _fail("calibration_status must be validated or diagnostic_only; unvalidated values are not accepted")

    defects = qa.get("defects", [])
    if not isinstance(defects, list):
        _fail("QA defects must be an array")
    for defect in defects:
        if not isinstance(defect, dict):
            _fail("Each QA defect must be an object")
        status = defect.get("status")
        if status not in {"fixed", "accepted"}:
            _fail(f"Unresolved defect blocks delivery: {defect.get('id', 'unknown')}")
        if defect.get("severity") == "critical" and status != "fixed":
            _fail(f"Critical defect must be fixed: {defect.get('id', 'unknown')}")
        if status == "accepted":
            approval = defect.get("approval")
            if not isinstance(approval, dict) or not approval.get("approved_by") or not approval.get("reason"):
                _fail(f"Accepted defect needs an approver and reason: {defect.get('id', 'unknown')}")

    delivery = qa.get("delivery")
    if not isinstance(delivery, dict):
        _fail("QA report requires a standalone delivery verification block")
    html_hash = hashlib.sha256(html_bytes).hexdigest()
    _check_sha(delivery.get("html_sha256"), "delivery.html_sha256")
    if delivery.get("html_sha256") != html_hash:
        _fail("QA HTML hash is stale or does not match the exact deliverable")
    if delivery.get("filename") != html_file.name:
        _fail("QA delivery filename does not match the final HTML file")
    required_true = ("standalone", "manifest_layer_ids_match", "asset_hashes_verified", "assets_loaded", "fonts_loaded", "critical_text_checked", "layer_geometry_checked", "z_order_checked", "reference_bounds_checked")
    for field in required_true:
        if delivery.get(field) is not True:
            _fail(f"QA delivery.{field} must be true")
    if delivery.get("external_dependencies") != []:
        _fail("QA delivery.external_dependencies must be an empty array")
    if delivery.get("canvas_overflow") is not False:
        _fail("QA must explicitly confirm no canvas overflow")
    if delivery.get("console_error_count") != 0:
        _fail("Browser console must have zero errors")
    if delivery.get("network_request_count") != 0:
        _fail("Standalone HTML must complete with zero runtime network requests")
    artboard = delivery.get("rendered_artboard")
    if not isinstance(artboard, dict):
        _fail("Browser QA must record the computed rendered artboard bounds")
    if artboard.get("x_px") != 0 or artboard.get("y_px") != 0 or artboard.get("width_px") != width or artboard.get("height_px") != height:
        _fail("Computed artboard bounds must match the exact native canvas at origin (0,0)")
    # Browser-measured layer geometry must cover every manifest layer exactly once.
    geometry_records = delivery.get("layer_geometry")
    if not isinstance(geometry_records, list):
        _fail("Browser QA must record computed geometry for every manifest layer")
    geometry_by_id = {item.get("id"): item for item in geometry_records if isinstance(item, dict)}
    if len(geometry_by_id) != len(geometry_records) or set(geometry_by_id) != set(manifest_ids):
        _fail("Computed layer geometry IDs must exactly match the frozen manifest")
    for layer in layers:
        layer_id = layer["id"]
        bbox = layer.get("bbox_px")
        if not isinstance(bbox, dict) or not all(k in bbox for k in ("x_min", "y_min", "x_max", "y_max")):
            _fail(f"Manifest layer {layer_id} requires a complete bbox_px")
        expected_bounds = {
            "x_px": bbox["x_min"],
            "y_px": bbox["y_min"],
            "width_px": bbox["x_max"] - bbox["x_min"],
            "height_px": bbox["y_max"] - bbox["y_min"]
        }
        record = geometry_by_id[layer_id]
        if record.get("status") != "pass":
            _fail(f"Browser-computed geometry failed for layer {layer_id}")
        for field, expected in expected_bounds.items():
            actual = record.get(field)
            if not isinstance(actual, (int, float)) or not math.isclose(float(actual), float(expected), rel_tol=0, abs_tol=1e-4):
                _fail(f"Browser-computed {field} for layer {layer_id} differs from the frozen manifest")

    # Computed stacking order must also match the manifest exactly.
    stack_records = delivery.get("layer_stack")
    if not isinstance(stack_records, list):
        _fail("Browser QA must record computed z-index for every manifest layer")
    stack_by_id = {item.get("id"): item for item in stack_records if isinstance(item, dict)}
    if len(stack_by_id) != len(stack_records) or set(stack_by_id) != set(manifest_ids):
        _fail("Computed layer stack IDs must exactly match the frozen manifest")
    for layer in layers:
        record = stack_by_id[layer["id"]]
        if record.get("status") != "pass" or record.get("z_index") != layer.get("z_index"):
            _fail(f"Computed z-index for layer {layer['id']} differs from the frozen manifest")

    # Every registered asset must have an explicit successful browser load result.
    asset_loads = delivery.get("asset_loads")
    if not isinstance(asset_loads, list):
        _fail("Browser QA must record runtime load state for every manifest asset")
    asset_loads_by_id = {item.get("asset_id"): item for item in asset_loads if isinstance(item, dict)}
    if len(asset_loads_by_id) != len(asset_loads) or set(asset_loads_by_id) != asset_ids:
        _fail("Browser asset-load records must exactly match manifest asset IDs")
    for asset_id, record in asset_loads_by_id.items():
        if record.get("status") != "pass":
            _fail(f"Runtime asset failed to load: {asset_id}")

    # A font family is required only when the manifest says an actual font is rendered.
    required_fonts = set()
    required_text = {}
    for layer in layers:
        typography = layer.get("typography") if isinstance(layer.get("typography"), dict) else {}
        recovery = typography.get("recovery_method")
        font_family = typography.get("font_family")
        if recovery in {"EXACT_FONT", "APPROVED_SUBSTITUTE"}:
            if not isinstance(font_family, str) or not font_family.strip():
                _fail(f"Typography layer {layer['id']} requires a recorded font_family")
            required_fonts.add(font_family)
        if layer.get("method") == "TYPOGRAPHY" and isinstance(layer.get("content"), str) and layer["content"]:
            required_text[layer["id"]] = layer["content"]
    font_checks = delivery.get("font_checks")
    if not isinstance(font_checks, list):
        _fail("Browser QA must record font loading checks")
    font_checks_by_name = {item.get("font_family"): item for item in font_checks if isinstance(item, dict)}
    if len(font_checks_by_name) != len(font_checks) or not required_fonts.issubset(font_checks_by_name):
        _fail("Browser font checks must cover every exact or substitute font used by the manifest")
    for font_family in required_fonts:
        if font_checks_by_name[font_family].get("status") != "pass":
            _fail(f"Font failed to load: {font_family}")

    # Verify every semantic text layer's rendered copy against the frozen manifest.
    text_checks = delivery.get("critical_text_checks")
    if not isinstance(text_checks, list):
        _fail("Browser QA must record exact text verification for typography layers")
    text_checks_by_id = {item.get("layer_id"): item for item in text_checks if isinstance(item, dict)}
    if len(text_checks_by_id) != len(text_checks) or set(text_checks_by_id) != set(required_text):
        _fail("Critical text check IDs must exactly match the manifest typography text layers")
    for layer_id, expected in required_text.items():
        record = text_checks_by_id[layer_id]
        if record.get("status") != "pass" or record.get("expected_text") != expected or record.get("actual_text") != expected:
            _fail(f"Rendered text does not exactly match manifest content for layer {layer_id}")

    regions = delivery.get("critical_regions")
    if not isinstance(regions, list) or not regions:
        _fail("At least one critical visual region must be explicitly checked")
    for region in regions:
        if not isinstance(region, dict) or region.get("status") != "pass":
            _fail("Every critical visual region must pass review")

    return {
        "status": "passed",
        "deliverable": html_file.name,
        "deliverable_count": 1,
        "sha256": html_hash,
        "canvas": {"width_px": width, "height_px": height},
        "layer_count": len(manifest_ids),
        "qa_status": "PASS",
        "qa_passes": ["structural", "fidelity", "finishing"],
        "calibration_profile": calibration_profile,
        "metric_acceptance_mode": calibration_status,
        "measured_metrics": measured,
        "metric_algorithm": METRIC_ALGORITHM,
        "metric_algorithm_version": METRIC_ALGORITHM_VERSION,
        "external_runtime_dependencies": 0,
        "network_requests": 0,
        "embedded_asset_hashes": len(asset_records),
        "user_delivery_policy": "one_verified_standalone_html_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("qa_report", type=Path)
    parser.add_argument("reference_image", type=Path)
    parser.add_argument("rendered_image", type=Path)
    args = parser.parse_args()
    try:
        result = validate_delivery(args.html, args.manifest, args.qa_report, args.reference_image, args.rendered_image)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
