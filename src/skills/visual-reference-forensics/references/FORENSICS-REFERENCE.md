# Visual forensics reference

## Coordinate contract

- Origin: top-left of the normalized source image.
- Units: source pixels unless explicitly noted.
- Bounding box: `x_min`, `y_min`, `x_max`, `y_max`.
- Derived width: `x_max - x_min`; derived height: `y_max - y_min`.
- Rotation/transform: store separately; do not bake into coordinates without noting the transform.
- Reference region: store both normalized coordinates and pixel coordinates if future scale-independent retrieval is useful.

## Image normalization

Record original width/height, normalized width/height, EXIF orientation, colour profile handling, alpha treatment, and transform. Do not discard the original or overwrite it with a normalized file.

## Geometry

Measure canvas edges, dominant alignment lines, text baselines, margins, repeated spacing, object aspect ratios, crop boundaries, negative space, overlap and clipping. For a rotated object, record a polygon or transform in addition to the axis-aligned bounding box.

## Colour and gradients

A global palette reports prominent colours, not their spatial placement. For a gradient, sample positions across the region and retain the coordinate/value pairs. Record whether the gradient is linear, radial, mesh-like, or unknown. A fitted gradient model is an estimate unless the sampling density and residual error support it.

## OCR and typography

OCR output contains text, region, confidence, language, and engine/version. Font identification remains a separate matching task. Store candidates and rationale using visible features such as x-height, terminal shapes, contrast, width, weight, tracking and line height. Preserve exact text separately from styling.

## Segmentation/detection

Grounding DINO can produce text-conditioned candidate detections; SAM-family segmentation can produce masks from prompts or candidate boxes. The mask is primary evidence; a bounding rectangle is a derived convenience. Record model, version, prompt, confidence, and manual corrections.

## Confidence scale

Use an explicit numeric confidence only when the method provides a calibrated score or a documented analyst scale. Suggested analyst scale: `0.90–1.00` directly measurable/high agreement; `0.70–0.89` strong estimate; `0.40–0.69` ambiguous; `<0.40` weak. Label this as an analyst rubric, not a model probability.
