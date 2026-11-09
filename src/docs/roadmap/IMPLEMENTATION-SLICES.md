# Visual engine implementation slices

This is a proposed order, not an authorization to provision services or implement all slices at once.

## P0-A: Evaluation foundation

- Define benchmark fixture schema and 24 rights-cleared pilot references.
- Add annotation format for required copy, regions, layer geometry, asset identity, and severity weights.
- Generate a 0.2.1 baseline scorecard with manual reviewer inputs.
- Gate: fixtures validate; hashes pinned; baseline report reproducible.

## P0-B: Intake and analysis

- Build image intake/normalization CLI.
- Preserve original input and output a normalized derivative.
- Implement global/multi-scale region extraction and coordinate transform ledger.
- Add OCR adapter interface, geometric primitives, colour sampler, and optional segmentation adapter.
- Gate: synthetic fixtures cover EXIF orientation, alpha, ICC profile, high-resolution tiling, crop mapping, and failure/unknown states.

## P0-C: Deterministic rendering

- Pin Playwright and browser version.
- Capture viewport, DPR, fonts, colour scheme, image hashes, animation state, and renderer profile.
- Require stable layer IDs in generated HTML/SVG.
- Capture element bounds, computed styles, and layer screenshots.
- Gate: two independent renders of frozen inputs produce stable geometry and expected raster differences under the pinned runtime.

## P0-D: Multi-metric QA

- Add exact pixel diff, mismatch ratio, SSIM, OCR checks, geometry measures, colour ΔE00, edge/contour metrics, and optional deep perceptual metrics.
- Add region aggregation and critical hard gates.
- Map connected diff regions to manifest layer IDs.
- Gate: known synthetic defects are detected and classified; no score-only pass can override a hard gate.

## P0-E: Controlled repair loop

- Generate ranked defect list and patch only implicated layers.
- Save before/after renders and metric reports.
- Re-evaluate adjacent regions for regressions.
- Stop when no high-severity defects remain, user-approved budget is reached, or score improvement stalls.
- Gate: benchmark A/B shows improvement over baseline without increased critical false negatives.

## P1: Accuracy extensions

- Dedicated typography candidate ranking and font measurement.
- Gradient-field estimation and compositing analysis.
- SAM 3 / SAM 2 segmentation and Grounding DINO detection adapters.
- DINOv2 dense feature correspondence.
- Asset candidate re-ranking with licence/provenance filters.
- Per-task model routing based on uncertainty, expected improvement, latency, and price.

## P2: Persistence and integrations

- Supabase tables and pgvector only after engine result schemas stabilize.
- R2 binary objects and immutable asset versions.
- Evidence-backed knowledge curation and retrieval.
- Figma mapping/round-trip and Notion projection after a tested source of truth exists.
- Optional MCP server only when real hosted tools/data/actions are available and secured.


## Mandatory cross-cutting release requirement: manual continuity

Every release slice must include a fallback path to continue the customer job in the current ChatGPT conversation when integrated services fail. The checkpoint schema, manual handoff generator, orchestrator rules, and service matrix are part of the product contract. Local offline recovery when ChatGPT itself is unavailable remains a separate implementation requirement.
