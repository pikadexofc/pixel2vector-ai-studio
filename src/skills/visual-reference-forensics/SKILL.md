---
name: visual-reference-forensics
description: Use when decomposing an image into measured, independently addressable visual components for layered HTML reconstruction.
---

# Visual Reference Forensics

## Product purpose

The goal is not merely to make HTML that resembles an image. The goal is to reconstruct the image as a proper design: each meaningful component must be separately identifiable, positioned and editable. The final artboard is fixed-size and non-responsive. Do not analyze the reference as a website screenshot unless the user explicitly requests a website reconstruction.
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Measure the reference before interpreting or rebuilding it. Separate observed facts from estimates and unknowns. Every important observation must identify its evidence source and confidence.

## Procedure

1. Preserve the original file and record the supplied filename separately from the byte-detected format. Record SHA-256, byte size, raw stored dimensions, colour mode, alpha channel, EXIF orientation and ICC profile hash (or null when absent).
2. Normalize EXIF orientation into a derivative. Record normalized dimensions and the orientation transform separately from raw dimensions so coordinates always refer to the normalized image.
3. Establish canvas coordinates: top-left origin; pixel units; bounding boxes represented as `x_min`, `y_min`, `x_max`, `y_max`; derive width and height from those edges.
4. Segment the composition into every meaningful independent component: backgrounds, separate photo subjects, foreground objects, text blocks, logos, illustrations, shapes, dividers, textures, borders, masks and overlays. Keep parent-child containment and occlusion relationships. Do not collapse multiple independently editable elements into one flattened layer, and do not over-fragment meaningless pixels.
5. Measure every layer box and its visual bounds: alignment, whitespace, margins, baselines, aspect ratios, crop boundaries, overlap, transforms, clipping and repeated spacing. Prefer multiple independent landmarks over visual intuition.
6. Extract text with OCR and preserve the recognized string, OCR engine/version, bounding box, confidence, language, and uncertainty. OCR does not identify an exact typeface.
7. Recover typography before substitution. Search for the exact font and compare actual rendered glyphs against the source. Store ranked candidates with evidence; font names alone are not proof of a match. OCR does not identify a typeface.
8. If the exact font cannot be obtained or renders visibly wrong, extract the visible glyphs/words from the source raster. Preserve original letterforms, widths, heights, slant, kerning, tracking, baselines, line breaks, ligatures and distress. Clean masks and vectorize to SVG paths where practical; use source-derived transparent raster glyph assets where vectorization would lose detail. Keep distress/halftone overlays separate when possible. Never claim the original font file was recovered when only raster glyph artwork was extracted.
9. Sample colors spatially. Palette tools can identify prominent colors, but they do not recover gradient direction or geometry. For gradients, record sample coordinates and values; fit a spatial model only when the samples support it.
10. Detect candidate visual regions and masks with suitable segmentation/detection tools when available. Keep detection confidence and source model. Convert masks into boxes only as a derived representation, preserving the original mask.
11. Decide which reference regions can be extracted as independent source assets, which need a separate generated PNG, and which are best reconstructed as HTML/CSS or SVG. Record this per layer.
12. Record all assumptions, uncertain regions, and missing evidence.

## Evidence classes

- `OBSERVED`: directly measurable or visually unambiguous.
- `DERIVED`: calculated from observations, such as width from bounding coordinates.
- `ESTIMATED`: plausible but uncertain, such as font family or gradient stop placement.
- `UNKNOWN`: insufficient evidence.

Do not upgrade `ESTIMATED` or `UNKNOWN` to `OBSERVED` through confident phrasing.

## Output

Create `analysis.json` conforming to `schemas/visual-analysis.schema.json`, with source hash, normalized dimensions, regions, text observations, color samples, gradient observations, typography candidates, geometry, confidence, and unresolved questions. Keep the analysis artifact internal. Then hand the result to the orchestrator for layer-manifest authoring. Do not deliver analysis JSON, crops, previews or extracted artifacts to the customer. The only final customer deliverable is a verified standalone HTML file.

See [forensics reference](references/FORENSICS-REFERENCE.md) for measurement methods, confidence rules, and known tool limitations.

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.
