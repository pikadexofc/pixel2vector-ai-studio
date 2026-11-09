---
name: visual-quality-assurance
description: Use when inspecting and verifying a layered HTML design against its original image before final HTML delivery.
---

# Visual Quality Assurance
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

A render is not verified until the reference and output are compared at matched native artboard dimensions and the findings are recorded. A visual impression alone is not a QA report. This is a static design artboard; do not add responsive/mobile layout tests or judge it by website performance scores.

## Controlled comparison

1. Confirm the reference and render use the same orientation, crop, canvas dimensions, colour space policy, and scale.
2. Render with a recorded browser, version, viewport, device scale factor, font availability, and asset set.
3. Reject dimension mismatch before pixel comparison; never rescale silently to hide layout errors.
4. Create a raw difference map and a thresholded difference map.
5. Report mismatch ratio independently from the per-pixel colour threshold. Record metric implementation/version and preprocessing. Pixelmatch's `threshold` is a pixel-level colour-distance decision parameter, not the percentage of mismatched pixels.
6. Measure global and region-weighted metrics. Small but critical text/logo regions may need a higher weight than large low-information backgrounds.
7. Use SSIM or other perceptual metrics as additional indicators, not replacements for visual inspection.
8. Inspect OCR text and text-region alignment where legibility or exact copy matters.
9. Group changed pixels into connected components to identify spatial defect regions.
10. Compare output against the frozen layer manifest; use it to locate which layers intersect defect regions.
11. Add region-level comparison for critical typography, wordmarks, logos, high-information illustrations and major imagery.
12. Apply a validated benchmark or user-approved project profile when one exists. Otherwise mark numerical metrics diagnostic-only and require the direct visual-review record described below; never invent thresholds.

## Three review passes

- **Pass 1, structural:** canvas dimensions, missing layers, incorrect geometry, clipping, overlaps, z-order, broken assets, font fallback, and overflow.
- **Pass 2, visual fidelity:** crop, colour, gradient, typography, spacing, contrast, shape, imagery, shadows, and blend behaviour.
- **Pass 3, finishing:** antialiasing, one-pixel alignment, edge quality, consistency, readability, small details, and delivery completeness.

## Defect lifecycle

Each defect has a stable ID, region, affected layer IDs, severity, observed evidence, expected state, proposed correction, verification method, and status. Correct one defect group at a time, rerender, and rerun the relevant tests. Preserve before/after evidence.

## Scoring and acceptance

Use named metrics and document thresholds. Do not present one composite score as objective truth unless its weights and acceptance threshold have been calibrated on representative designs. Maintain hard gates for missing text, broken assets, canvas mismatch, licence problems, and other critical defects.

A final delivery requires all three passes (`structural`, `fidelity`, `finishing`), matched source/render dimensions, recorded pixel mismatch ratio, MAE and SSIM, a separate per-pixel threshold, named algorithm/version, all critical regions passing, zero console errors, loaded fonts/assets, zero canvas overflow, no open/deferred critical defects and an exact final HTML SHA-256 match. Apply calibrated numerical thresholds when a validated benchmark or approved project profile exists. Without one, mark numerical metrics diagnostic-only and require a direct visual-review record bound to the exact reference and render hashes, recording all three passes and critical regions reviewed; never invent thresholds or present uncalibrated metrics as objective pass/fail truth. `PASS_WITH_EXCEPTIONS`, `FAIL` and `BLOCKED` do not authorize delivery. `PIXEL_IDENTICAL` requires exact pixel equality, not merely high SSIM.

## Internal QA output and customer delivery

Produce internal QA evidence conforming to `schemas/standalone-html-delivery.schema.json`, including measured metrics, threshold mode, direct visual-review evidence, three passes, region checks, defects, environment and the final HTML hash. Run `scripts/validate_standalone_delivery.py` as the release gate. Never deliver the QA report, difference maps, previews or manifests. The only user-facing artifact is the final verified standalone HTML file. If the gate fails, deliver no file and state the blocker concisely. See [QA methods](references/QA-METHODS.md) and `resources/FINAL-HTML-ONLY-DELIVERY.md`.

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.
