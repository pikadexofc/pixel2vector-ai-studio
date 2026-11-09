# PixelPerfect Studio agent instructions

## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. User task completion comes first. Usage metering is best-effort and must not block or interrupt an in-progress request. Deliver the answer first; reconcile usage, entitlements, reminders, and analytics afterward. Preserve context and continue manually in ChatGPT when available.

## Mission

Convert a flat image into a high-fidelity, editable, fixed-size HTML design. The HTML is a structured design artboard, not a responsive website. Keep every meaningful component independently addressable as HTML/CSS, SVG or a separately embedded PNG/image layer. Extract source visuals first; generate individual PNG assets when extraction cannot meet quality. Prioritize visual fidelity and component quality over website optimization. Deliver exactly one final verified standalone HTML file.

## Source-of-truth ownership

- Project/layer/asset/evidence/QA metadata: Supabase PostgreSQL when configured.
- Binary assets: Cloudflare R2 when configured.
- Source, schemas, scripts, tests, skills, and decisions: GitHub.
- Human-readable views: Notion, never a competing machine source of truth.
- Current project brief and approved frozen layer manifest: authority for a single reconstruction.

These services are selected architecture, not guaranteed connections. Check tools and account availability before claiming access.

## Workflow routing

Use `setup` for intake, `pixelperfect-orchestrator` for multi-stage work, and the relevant specialist Skills for forensics, assets, compilation, QA, memory, design-system, workspace, and Figma tasks. Do not perform final compilation before the layer manifest and assets are approved/frozen.

## Engineering rules

- Inspect existing files and instructions before modifying a workspace.
- For code changes, use test-first development: failing test, verify failure, minimal implementation, verify pass, full suite.
- For skill changes, check frontmatter, local references, activation scope, and representative behavioural cases.
- Validate JSON schemas and example records before release.
- Build deterministic packages twice and compare hashes when repeatability is required.
- Extract the final ZIP to a clean directory and validate again.
- Never weaken a check to force a pass.

## Evidence and visual accuracy

- Preserve source references and hashes.
- Prefer extracting/masking source-specific visual material before generating substitutes.
- Search for the exact font first. If unavailable or visually wrong, extract source glyphs and use SVG paths or transparent raster glyph artwork; never mislabel glyph artwork as a recovered font.
- Normalize EXIF orientation before coordinate analysis.
- Use top-left pixel coordinates and `x_min/y_min/x_max/y_max` boxes.
- OCR does not establish exact font identity; palette extraction does not establish gradient geometry.
- Record source/licence, confidence, tool version and unknowns.
- Distinguish Pixelmatch per-pixel threshold from overall mismatch ratio.
- Never call output pixel-perfect without exact-size rendering and independent inspection.

## Reconstruction delivery rule

- Deliver exactly one final verified standalone HTML file. Keep previews, manifests, source files, assets, fonts, reports, QA evidence, checkpoints and ZIP bundles internal.
- If the final verification gate cannot pass, deliver no HTML candidate and state the specific blocker.
- Final approval requires exact source/render dimensions, a frozen manifest, exact HTML/manifest layer IDs, browser-computed geometry and z-order checks, exact text checks, asset/font load checks, three QA passes, recomputed comparison metrics, direct visual review bound to the exact source/render hashes, no unresolved critical defects, and a final HTML hash match. Apply a calibrated metric profile when one exists; otherwise mark metrics diagnostic-only and rely on the required hash-bound three-pass visual review. Never fabricate thresholds.

## Security and permissions

- No credentials, tokens, client-private assets, or sensitive personal context in the package.
- Do not provision Supabase/Cloudflare, modify external accounts, push source, deploy, or publish without explicit authorization.
- Do not claim a host tool ran unless the host returned execution evidence.
- Maintain original assets as immutable; process derivatives as new versions.

## Manual continuity requirement

- Treat a blocked integration as a service degradation, not an automatic job failure.
- When ChatGPT remains available, use `manual-fallback-continuity` to continue the same task manually with accessible references and host capabilities.
- Preserve progress in a validated continuity checkpoint. Never include credentials, tokens, signed URLs, or binary source data in it.
- Never claim an unavailable upload, API call, OCR run, segmentation, render, metric, database write, Figma operation, or deployment succeeded.
- If ChatGPT itself is unavailable, preserve local internal project files and a private checkpoint for later resumption. Do not expose recovery files as reconstruction deliverables or promise background execution.

## Completion report

Report exact outputs, executed commands and results, hashes, skipped checks, assumptions, known limitations, and any external approvals still required.
