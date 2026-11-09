# Visual QA methods

## Mandatory metadata

Reference hash, render hash, width/height, orientation, colour-space policy, browser/version, viewport, device scale factor, font set, asset-set hash, comparison algorithm/version, threshold settings, and date/time.

## Pixel difference

Pixelmatch's per-pixel threshold classifies individual pixel differences. Calculate mismatch ratio separately:

`mismatch_ratio = mismatched_pixels / total_compared_pixels`

Do not call the configured per-pixel threshold a percentage. Record antialiasing policy and alpha handling. Never resize an image to force a match without recording the transform.

## Region weighting

Partition the image into semantically meaningful regions, score each independently, and use explicit weights when a global score is required. Store region weight and reason. Critical text or brand marks may be treated as hard gates instead of allowing large flat backgrounds to dominate the average.

## Supporting metrics

- SSIM: structural similarity indicator.
- OCR comparison: text content and location drift.
- Connected components: spatially group changed pixels into candidate defects.
- Edge/geometry comparison: help distinguish boundary shifts from colour-only changes.
- Human visual review: inspect actual differences; algorithmic metrics are not a substitute.

## Three-pass checklist

### Structural
Canvas, region bounds, missing/extra layers, z-index, clipping, overflow, masks, transforms, fonts and asset loading.

### Fidelity
Text, type style, imagery/crop, palette, gradients, spacing, composition, borders, shadows, contrast and blend modes.

### Finishing
Antialiasing, fractional coordinates, optical alignment, line wraps, small labels, icon sharpness, one-pixel defects and final packaging.

## Status

- `PASS`: all hard gates pass and residual metrics meet documented tolerance.
- `PASS_WITH_EXCEPTIONS`: internal review can record user-accepted noncritical defects, but this status does not authorize final HTML delivery. The final standalone-delivery gate requires `PASS`.
- `FAIL`: a hard gate fails or a critical defect remains.
- `BLOCKED`: comparison cannot be performed reliably because an input or tool is missing.


## Final-delivery gate

The release validator recomputes mismatch ratio, RGB MAE and SSIM from the exact reference and render files. The pixel threshold is a per-pixel RGB max-channel distance and is not the mismatch percentage. Numeric tolerances must be supplied by a validated benchmark or explicit user-approved profile. If no such profile exists, mark the metrics diagnostic-only and bind a direct three-pass visual review to the exact reference and render hashes, including the critical regions inspected. A generic sample threshold is never a valid production default.
