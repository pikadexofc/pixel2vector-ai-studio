# Visual fidelity scorecard contract

**Status:** proposed, requires calibration on the PixelPerfect benchmark.

## Hard gates

A release fails when any critical condition occurs:

- Canvas dimensions/orientation differ from the requested target.
- Required copy is missing, altered, or unreadable.
- A critical visual layer is missing, extra, or materially occluded.
- A critical logo/product/subject is substituted without permission.
- A required asset is broken, clipped, or outside the delivery artboard.
- An external asset has no acceptable rights/provenance record.

## Candidate normalized dimensions

| Dimension | Proposed pilot weight | Candidate signals |
|---|---:|---|
| Geometry and layout | 25% | BBox IoU, landmark/centre displacement, baseline/spacing error, edge overlap |
| Text and typography | 20% | Exact-string check, CER/WER, OCR box IoU, line count/order, rendered width and baseline error |
| Asset and crop fidelity | 15% | Asset identity/crop labels, DINOv2 regional matching, mask IoU |
| Colour and gradients | 15% | Regional ΔE00, sampled gradient field deviation, alpha/compositing checks |
| Edges and fine detail | 10% | Edge F1, contour distance, boundary F-score, one-pixel defect counts |
| Perceptual structure | 15% | SSIM/MS-SSIM plus suitable LPIPS/DISTS/DreamSim signals |

The weights are starting hypotheses. The score is not validated until it correlates with blind expert rankings on held-out references. Different design classes may require different profiles.

## Scoring rules

- Keep every raw metric in its native scale in the report.
- Normalize only with a documented benchmark-specific transform.
- Report component scores next to the composite, not just the final number.
- Keep hard gates outside the weighted sum.
- Compute both global and region-level scores.
- Weight regions by user-brief criticality and visual salience, not only pixel area.
- Never allow LPIPS, DreamSim, DINOv2, or CLIP to override exact copy or geometry requirements.
- Calculate pixel mismatch ratio separately from Pixelmatch's per-pixel threshold.
- Do not align/warp the render before primary scoring. A diagnostic alignment result may be reported separately.

## Calibration protocol

1. Gather a diverse rights-cleared reference corpus.
2. Generate outputs from the baseline and each candidate workflow.
3. Collect at least two independent blind pairwise judgments for a representative subset.
4. Record per-dimension reviewer ratings and critical defects.
5. Compute Spearman/Kendall rank correlation between metric rankings and reviewer rankings.
6. Check correlation, false negatives, and inter-rater agreement per design class.
7. Fit or adjust weights on a development split only.
8. Freeze the weighting transform and evaluate on a held-out split.
9. Version the metrics, thresholds, weights, and benchmark fixture hashes.

## Defect record minimum

Each defect must contain:

- stable defect ID and severity
- reference/render hashes
- region and layer IDs
- defect category
- raw evidence path (diff, OCR output, mask, or geometry comparison)
- metric name/version/threshold
- confidence and known limitations
- proposed correction and affected layer scope
- verification result after the repair
