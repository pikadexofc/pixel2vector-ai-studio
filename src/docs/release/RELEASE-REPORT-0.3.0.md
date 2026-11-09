# Release Report 0.3.0

**Release date:** 2026-11-03
**Type:** Major workflow and delivery-contract upgrade
**Base:** 0.2.4

## Product behavior

- Reconstruction handoff is restricted to exactly one final, verified, offline-capable standalone HTML file.
- Previews, assets, crops, masks, fonts, manifests, source code, stage ledgers, reports, difference maps, checkpoints and ZIP project bundles remain internal.
- If the final acceptance gate cannot pass, no HTML candidate is delivered. The blocker is stated briefly.

## Incorporated learning

- Three reconstruction exercises and their learning archive are preserved under `knowledge/reconstruction-baseline-v1.0/`.
- Source-derived visual extraction is preferred over generating replacements when clean recovery is possible.
- Typography recovery searches for the exact font first, then uses source-derived glyph raster/SVG artwork when exact font recovery fails. Extracted letterforms are not described as a recovered font file.
- Original filename and byte-detected image format are stored separately.
- Frozen manifest geometry and unique layer IDs must exactly match HTML `data-layer` IDs.
- Layer counts and documentation must be generated from the manifest.
- QA includes structural, fidelity and finishing passes plus recomputed metrics from real source/render files and calibrated acceptance thresholds.
- A rendered page is not automatically a verified reconstruction.

## New release gate

`scripts/validate_standalone_delivery.py` checks the exact HTML hash, detected source/render file formats, source byte size/hash/raw and EXIF-normalized dimensions/orientation/ICC profile, frozen canvas size, exact manifest-to-HTML layer IDs, browser-computed per-layer geometry and z-index, byte-identical embedded asset hashes, browser asset/font load evidence, exact rendered typography text, offline runtime, recomputed mismatch ratio/MAE/SSIM, calibrated thresholds, three QA passes, defect closure, browser errors, network requests, artboard bounds and critical regions.

The gate does not assert a universal similarity threshold. Acceptance profiles must be user-approved or benchmark-validated. `PIXEL_IDENTICAL` remains a separate claim requiring exact pixel equality.

## Validation outcome

- Plugin validator: **PASS**, version 0.3.0, 11 Skills, 120 packaged files, four brand asset declarations checked, 10 local Markdown links checked.
- Schema/example validation: **PASS**, all nine bundled JSON examples plus plugin manifest.
- Automated regression suite: **PASS**, 28 tests.
- Import archive: **PASS**, ZIP CRC/integrity check, one top-level `pixelperfect-studio/` folder, both manifests at version 0.3.0, tests and learning evidence included.
- Reproducibility: **PASS**, two consecutive builds produced identical SHA-256 hashes.
- Clean extraction: **PASS**, plugin validation, example validation and all 28 tests passed from the extracted archive.

**Not verified:** ChatGPT desktop/plugin UI import was not exercised. Public Plugin Directory listing and publisher approval were not attempted. This package is not publicly published.
