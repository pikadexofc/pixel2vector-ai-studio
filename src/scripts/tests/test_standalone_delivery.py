import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.validate_standalone_delivery import (
    validate_delivery, DeliveryValidationError, _calculate_metrics,
    METRIC_ALGORITHM, METRIC_ALGORITHM_VERSION
)


class StandaloneDeliveryGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.html = self.root / "final.html"
        self.manifest = self.root / "layer-manifest.json"
        self.qa = self.root / "qa-report.json"
        self.reference = self.root / "reference.png"
        self.render = self.root / "render.png"
        self.html_text = (
            '<!doctype html><html><head><meta charset="utf-8">'
            '<style>@font-face{font-family:Demo;src:url(data:font/woff2;base64,AA==)}'
            '.artboard{width:32px;height:32px}</style></head><body>'
            '<main class="artboard" data-artboard="true" data-canvas-width="32" data-canvas-height="32"></main>'
            '<div data-layer="background"></div><h1 data-layer="headline">Test</h1>'
            '</body></html>'
        )
        self.html.write_text(self.html_text, encoding="utf-8")
        self.manifest.write_text(json.dumps({
            "status": "frozen",
            "canvas": {"width_px": 32, "height_px": 32},
            "layers": [
                {"id": "background", "type": "shape", "bbox_px": {"x_min": 0, "y_min": 0, "x_max": 32, "y_max": 32}, "z_index": 0, "method": "CODE", "asset_id": None},
                {"id": "headline", "type": "text", "bbox_px": {"x_min": 1, "y_min": 1, "x_max": 31, "y_max": 11}, "z_index": 10, "method": "TYPOGRAPHY", "asset_id": None, "content": "Test", "typography": {"recovery_method": "SOURCE_GLYPH_SVG", "font_verified": False}}
            ],
            "assets": []
        }), encoding="utf-8")
        pixels = np.zeros((32, 32, 3), dtype=np.uint8)
        pixels[:, :, :] = [240, 232, 220]
        Image.fromarray(pixels, "RGB").save(self.reference, format="PNG")
        Image.fromarray(pixels, "RGB").save(self.render, format="PNG")
        manifest = json.loads(self.manifest.read_text())
        manifest["source"] = {
            "filename": self.reference.name,
            "detected_format": "PNG",
            "sha256": hashlib.sha256(self.reference.read_bytes()).hexdigest(),
            "byte_size": self.reference.stat().st_size,
            "width_px": 32,
            "height_px": 32,
            "normalized_width_px": 32,
            "normalized_height_px": 32,
            "exif_orientation": 1,
            "exif_orientation_transform": None,
            "icc_profile_sha256": None,
            "mode": "RGB"
        }
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        self.write_qa()

    def write_qa(self):
        metrics = _calculate_metrics(self.reference, self.render, 24)
        manifest = json.loads(self.manifest.read_text())
        layer_geometry = []
        layer_stack = []
        critical_text_checks = []
        font_checks = []
        for layer in manifest["layers"]:
            bbox = layer["bbox_px"]
            layer_geometry.append({
                "id": layer["id"], "x_px": bbox["x_min"], "y_px": bbox["y_min"],
                "width_px": bbox["x_max"] - bbox["x_min"], "height_px": bbox["y_max"] - bbox["y_min"], "status": "pass"
            })
            layer_stack.append({"id": layer["id"], "z_index": layer["z_index"], "status": "pass"})
            if layer.get("method") == "TYPOGRAPHY" and layer.get("content"):
                critical_text_checks.append({"layer_id": layer["id"], "expected_text": layer["content"], "actual_text": layer["content"], "status": "pass"})
            typography = layer.get("typography", {})
            if typography.get("recovery_method") in {"EXACT_FONT", "APPROVED_SUBSTITUTE"}:
                font_checks.append({"font_family": typography["font_family"], "status": "pass"})
        qa = {
            "status": "PASS",
            "reference": {
                "sha256": hashlib.sha256(self.reference.read_bytes()).hexdigest(),
                "width_px": 32, "height_px": 32, "detected_format": "PNG"
            },
            "render": {
                "sha256": hashlib.sha256(self.render.read_bytes()).hexdigest(),
                "width_px": 32, "height_px": 32, "detected_format": "PNG"
            },
            "environment": {"browser": "Chromium", "version": "123.0.0.0", "device_scale_factor": 1},
            "comparison": {
                "algorithm": METRIC_ALGORITHM,
                "algorithm_version": METRIC_ALGORITHM_VERSION,
                "preprocessing": "native dimensions, EXIF-normalized, sRGB RGB",
                "pixel_threshold_rgb": 24,
                **metrics,
                "acceptance_thresholds": {
                    "profile_id": "diagnostic-only",
                    "calibration_status": "diagnostic_only",
                    "source": "diagnostic_only"
                }
            },
            "passes": ["structural", "fidelity", "finishing"],
            "visual_review": {
                "status": "PASS",
                "method": "direct_visual_inspection",
                "reviewer": "host_visual_reviewer",
                "reference_sha256": hashlib.sha256(self.reference.read_bytes()).hexdigest(),
                "render_sha256": hashlib.sha256(self.render.read_bytes()).hexdigest(),
                "passes": ["structural", "fidelity", "finishing"],
                "critical_regions_reviewed": ["headline", "background"]
            },
            "defects": [],
            "delivery": {
                "filename": "final.html",
                "html_sha256": hashlib.sha256(self.html.read_bytes()).hexdigest(),
                "standalone": True,
                "external_dependencies": [],
                "manifest_layer_ids_match": True,
                "asset_hashes_verified": True,
                "assets_loaded": True,
                "fonts_loaded": True,
                "critical_text_checked": True,
                "layer_geometry_checked": True,
                "z_order_checked": True,
                "reference_bounds_checked": True,
                "canvas_overflow": False,
                "console_error_count": 0,
                "network_request_count": 0,
                "rendered_artboard": {"x_px": 0, "y_px": 0, "width_px": manifest["canvas"]["width_px"], "height_px": manifest["canvas"]["height_px"]},
                "layer_geometry": layer_geometry,
                "layer_stack": layer_stack,
                "asset_loads": [{"asset_id": item["asset_id"], "status": "pass"} for item in manifest.get("assets", [])],
                "font_checks": font_checks,
                "critical_text_checks": critical_text_checks,
                "critical_regions": [{"name": "headline", "status": "pass"}]
            }
        }
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        return qa

    def tearDown(self):
        self.tmp.cleanup()

    def validate(self):
        return validate_delivery(self.html, self.manifest, self.qa, self.reference, self.render)

    def test_accepts_a_verified_single_file_standalone_html(self):
        result = self.validate()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["deliverable_count"], 1)
        self.assertEqual(result["deliverable"], "final.html")

    def test_rejects_manifest_html_layer_id_mismatch(self):
        self.html.write_text(self.html_text.replace('data-layer="headline"', 'data-layer="title"'), encoding="utf-8")
        self.write_qa()
        with self.assertRaisesRegex(DeliveryValidationError, "layer mismatch"):
            self.validate()

    def test_rejects_external_runtime_assets(self):
        self.html.write_text(self.html_text.replace('</head>', '<script src="https://cdn.example/x.js"></script></head>'), encoding="utf-8")
        self.write_qa()
        with self.assertRaisesRegex(DeliveryValidationError, "runtime dependencies"):
            self.validate()

    def test_rejects_relative_runtime_assets(self):
        self.html.write_text(self.html_text.replace('</body>', '<img src="assets/photo.png"></body>'), encoding="utf-8")
        self.write_qa()
        with self.assertRaisesRegex(DeliveryValidationError, "runtime dependencies"):
            self.validate()

    def test_rejects_network_calls_in_inline_javascript(self):
        self.html.write_text(self.html_text.replace('</body>', '<script>fetch("https://example.com")</script></body>'), encoding="utf-8")
        self.write_qa()
        with self.assertRaisesRegex(DeliveryValidationError, "network-capable"):
            self.validate()

    def test_rejects_external_css_imports(self):
        self.html.write_text(self.html_text.replace('</style>', '@import url(https://cdn.example/font.css);</style>'), encoding="utf-8")
        self.write_qa()
        with self.assertRaisesRegex(DeliveryValidationError, "runtime dependencies"):
            self.validate()

    def test_detects_file_format_from_bytes_not_filename_extension(self):
        pixels = np.zeros((32, 32, 3), dtype=np.uint8)
        pixels[:, :, :] = [240, 232, 220]
        Image.fromarray(pixels, "RGB").save(self.reference, format="JPEG")  # Deliberately keep .png filename.
        qa = self.write_qa()
        qa["reference"]["detected_format"] = "JPEG"
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        manifest = json.loads(self.manifest.read_text())
        manifest["source"].update({
            "detected_format": "JPEG",
            "sha256": hashlib.sha256(self.reference.read_bytes()).hexdigest(),
            "byte_size": self.reference.stat().st_size
        })
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        result = self.validate()
        self.assertEqual(result["status"], "passed")

    def test_rejects_format_metadata_that_conflicts_with_file_bytes(self):
        pixels = np.zeros((32, 32, 3), dtype=np.uint8)
        pixels[:, :, :] = [240, 232, 220]
        Image.fromarray(pixels, "RGB").save(self.reference, format="JPEG")
        qa = self.write_qa()
        qa["reference"]["detected_format"] = "JPEG"
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        manifest = json.loads(self.manifest.read_text())
        manifest["source"].update({
            "sha256": hashlib.sha256(self.reference.read_bytes()).hexdigest(),
            "byte_size": self.reference.stat().st_size
        })
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "Manifest source.detected_format"):
            self.validate()

    def test_rejects_canvas_dimension_mismatch(self):
        pixels = np.zeros((31, 32, 3), dtype=np.uint8)
        Image.fromarray(pixels, "RGB").save(self.render, format="PNG")
        with self.assertRaises(DeliveryValidationError):
            self.validate()

    def test_accepts_diagnostic_metrics_with_bound_three_pass_visual_review(self):
        qa = self.write_qa()
        self.assertEqual(qa["comparison"]["acceptance_thresholds"]["calibration_status"], "diagnostic_only")
        result = self.validate()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["calibration_profile"], "diagnostic_only_visual_review")

    def test_accepts_validated_profile_when_metrics_meet_limits(self):
        qa = self.write_qa()
        qa["comparison"]["acceptance_thresholds"] = {
            "profile_id": "strict-poster-v1",
            "calibration_status": "validated",
            "source": "validated_profile",
            "max_mismatch_ratio": 0.03,
            "max_mae": 3.0,
            "min_ssim": 0.97
        }
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        result = self.validate()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["metric_acceptance_mode"], "validated")

    def test_rejects_unvalidated_threshold_status(self):
        qa = self.write_qa()
        qa["comparison"]["acceptance_thresholds"]["calibration_status"] = "unvalidated"
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "diagnostic_only"):
            self.validate()

    def test_rejects_missing_direct_visual_review(self):
        qa = self.write_qa()
        del qa["visual_review"]
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "visual_review"):
            self.validate()

    def test_rejects_visual_review_bound_to_different_render(self):
        qa = self.write_qa()
        qa["visual_review"]["render_sha256"] = "0" * 64
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "reviewed render hash"):
            self.validate()

    def test_rejects_failed_direct_visual_review(self):
        qa = self.write_qa()
        qa["visual_review"]["status"] = "FAIL"
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "visual_review must record PASS"):
            self.validate()

    def test_rejects_metrics_outside_approved_thresholds(self):
        pixels = np.zeros((32, 32, 3), dtype=np.uint8)
        pixels[:, :, :] = [0, 0, 0]
        Image.fromarray(pixels, "RGB").save(self.render, format="PNG")
        qa = self.write_qa()
        qa["comparison"]["acceptance_thresholds"] = {
            "profile_id": "strict-poster-v1",
            "calibration_status": "validated",
            "source": "validated_profile",
            "max_mismatch_ratio": 0.03,
            "max_mae": 3.0,
            "min_ssim": 0.97
        }
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "outside the calibrated"):
            self.validate()

    def test_rejects_tampered_metric_record(self):
        qa = self.write_qa()
        qa["comparison"]["mismatch_ratio"] = 0.1
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "does not match recomputed"):
            self.validate()

    def test_rejects_browser_layer_geometry_drift(self):
        qa = self.write_qa()
        qa["delivery"]["layer_geometry"][1]["x_px"] += 1
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "differs from the frozen manifest"):
            self.validate()

    def test_rejects_browser_z_order_drift(self):
        qa = self.write_qa()
        qa["delivery"]["layer_stack"][1]["z_index"] = 9
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "z-index"):
            self.validate()

    def test_rejects_text_that_differs_from_frozen_manifest(self):
        qa = self.write_qa()
        qa["delivery"]["critical_text_checks"][0]["actual_text"] = "Test typo"
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "does not exactly match manifest content"):
            self.validate()

    def _add_embedded_asset(self):
        import base64
        import io
        image_buffer = io.BytesIO()
        Image.new("RGB", (2, 2), (12, 34, 56)).save(image_buffer, format="PNG")
        asset_bytes = image_buffer.getvalue()
        data_uri = "data:image/png;base64," + base64.b64encode(asset_bytes).decode("ascii")
        self.html_text = self.html_text.replace("</body>", f'<img alt="embedded" src="{data_uri}"></body>')
        self.html.write_text(self.html_text, encoding="utf-8")
        manifest = json.loads(self.manifest.read_text())
        manifest["layers"][0]["asset_id"] = "asset-background"
        manifest["assets"] = [{"asset_id": "asset-background", "sha256": hashlib.sha256(asset_bytes).hexdigest()}]
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        return self.write_qa()

    def test_accepts_manifest_asset_when_embedded_and_browser_loaded(self):
        self._add_embedded_asset()
        result = self.validate()
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["embedded_asset_hashes"], 1)

    def test_rejects_asset_that_browser_did_not_load(self):
        qa = self._add_embedded_asset()
        qa["delivery"]["asset_loads"][0]["status"] = "fail"
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "Runtime asset failed to load"):
            self.validate()

    def test_requires_font_load_evidence_for_exact_font(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["layers"][1]["typography"] = {"recovery_method": "EXACT_FONT", "font_family": "Inter", "font_verified": True}
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        qa = self.write_qa()
        qa["delivery"]["font_checks"] = []
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "font checks must cover"):
            self.validate()

    def test_rejects_font_that_failed_to_load(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["layers"][1]["typography"] = {"recovery_method": "EXACT_FONT", "font_family": "Inter", "font_verified": True}
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        qa = self.write_qa()
        qa["delivery"]["font_checks"][0]["status"] = "fail"
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "Font failed to load"):
            self.validate()

    def test_rejects_open_defects(self):
        qa = self.write_qa()
        qa["defects"] = [{"id": "D-1", "severity": "major", "status": "open", "description": "bad crop"}]
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "Unresolved defect"):
            self.validate()

    def test_rejects_pass_with_exceptions(self):
        qa = self.write_qa()
        qa["status"] = "PASS_WITH_EXCEPTIONS"
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "status must be PASS"):
            self.validate()

    def test_rejects_stale_html_hash(self):
        qa = self.write_qa()
        qa["delivery"]["html_sha256"] = "c" * 64
        self.qa.write_text(json.dumps(qa))
        with self.assertRaisesRegex(DeliveryValidationError, "hash is stale"):
            self.validate()

    def test_accepts_exif_rotated_source_when_normalized_canvas_is_exact(self):
        raw = np.zeros((24, 32, 3), dtype=np.uint8)
        raw[:, :, :] = [210, 190, 170]
        exif = Image.Exif()
        exif[274] = 6
        Image.fromarray(raw, "RGB").save(self.reference, format="JPEG", quality=100, exif=exif)
        normalized = np.asarray(ImageOps.exif_transpose(Image.open(self.reference)).convert("RGB"))
        render = Image.fromarray(normalized, "RGB")
        render.save(self.render, format="PNG")
        self.html_text = self.html_text.replace('width:32px;height:32px', 'width:24px;height:32px')
        self.html_text = self.html_text.replace('data-canvas-width="32" data-canvas-height="32"', 'data-canvas-width="24" data-canvas-height="32"')
        self.html.write_text(self.html_text, encoding="utf-8")
        manifest = json.loads(self.manifest.read_text())
        manifest["canvas"].update({"width_px": 24, "height_px": 32})
        manifest["layers"][0]["bbox_px"].update({"x_max": 24, "y_max": 32})
        manifest["layers"][1]["bbox_px"].update({"x_max": 23})
        manifest["source"].update({
            "detected_format": "JPEG",
            "sha256": hashlib.sha256(self.reference.read_bytes()).hexdigest(),
            "byte_size": self.reference.stat().st_size,
            "width_px": 32,
            "height_px": 24,
            "normalized_width_px": 24,
            "normalized_height_px": 32,
            "exif_orientation": 6,
            "exif_orientation_transform": "EXIF orientation 6 normalized to display orientation"
        })
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        qa = self.write_qa()
        qa["reference"].update({"width_px": 24, "height_px": 32, "detected_format": "JPEG"})
        qa["render"].update({"width_px": 24, "height_px": 32, "detected_format": "PNG"})
        qa["delivery"]["rendered_artboard"].update({"width_px": 24, "height_px": 32})
        self.qa.write_text(json.dumps(qa), encoding="utf-8")
        result = self.validate()
        self.assertEqual(result["canvas"], {"width_px": 24, "height_px": 32})

    def test_rejects_source_normalized_dimension_mismatch(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["source"]["normalized_width_px"] = 31
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "normalized dimensions"):
            self.validate()

    def test_rejects_manifest_source_hash_mismatch(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["source"]["sha256"] = "d" * 64
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(DeliveryValidationError, "source.sha256 does not match"):
            self.validate()

    def test_rejects_unfrozen_manifest(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["status"] = "draft"
        self.manifest.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(DeliveryValidationError, "must be frozen"):
            self.validate()

    def test_rejects_layer_asset_reference_without_asset_record(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["layers"][1]["asset_id"] = "missing-asset"
        self.manifest.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(DeliveryValidationError, "missing manifest assets"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
