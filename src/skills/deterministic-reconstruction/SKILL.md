---
name: deterministic-reconstruction
description: Use when assembling separate visual layers and PNG assets into one fixed-size editable standalone HTML design.
---

# Deterministic Reconstruction Compiler

## HTML is the design document, not a website

Compile a fixed-size visual artboard whose meaningful components are independently addressable. Do not add responsive breakpoints, mobile reflow, website navigation, app behavior, SEO features, hover effects or optimization that changes the source appearance. This workflow prioritizes visual fidelity and quality over website engineering metrics. Preserve the exact artboard composition at its native dimensions.
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

The compiler converts a validated, frozen manifest and immutable asset versions into a reproducible output. It does not invent missing design decisions or silently change the approved composition.

## Preconditions

Require:
- normalized reference dimensions and coordinate convention
- approved layer manifest with stable IDs and geometry
- selected assets with hashes and rights records
- declared font availability/fallbacks
- render viewport, device scale factor, browser/runtime version, and output target
- unresolved defects and assumptions explicitly recorded

If these are absent, return a compile-readiness report rather than guessing.

## Compilation procedure

1. Validate manifest schema, IDs, parent relationships, geometry, z-index, transforms, clipping, and references.
2. Confirm the manifest canvas dimensions equal the approved target dimensions.
3. Resolve all referenced assets by stable ID and content hash. Reject missing, changed, or licence-incompatible assets.
4. Build a fixed artboard with explicit width/height in CSS pixels, origin, overflow, background, and stacking context.
5. Convert each meaningful component to its declared rendering primitive: its own embedded PNG/image, live text, source-glyph artwork, SVG, CSS shape, mask, background or generated component. Separate image assets must remain separate DOM image layers, not be baked together into a composite.
5a. Typography is source-fidelity-critical: search for the exact font, test real glyph rendering, then extract glyphs from the image if exact font recovery fails. Do not silently substitute a visually different typeface.
6. Preserve absolute geometry and z-order. Use transforms only when explicitly recorded. Use artboard-scoped CSS selectors; broad selectors must never override per-layer geometry. Give each independently editable component a stable `data-layer` identifier, a named class and its own DOM element. Define explicit z-index bands and test overlapping critical layers.
7. Encode typography settings explicitly: family and fallback, size, weight, tracking, line height, alignment, casing, and text box geometry.
8. Keep gradients, blend modes, opacity, masks, and shadows as explicit properties rather than inferred defaults.
9. Embed every PNG, SVG, font, texture and other required resource individually for offline rendering. Preserve image quality; do not aggressively downscale, quantize or recompress assets when that changes visible details. Avoid remote images, remote fonts, external stylesheets or scripts.
10. Generate one self-contained standalone HTML file with all required assets, SVG, styles and fonts embedded. The layer manifest and asset register remain internal build inputs; do not require a companion file at runtime.
11. Record compiler version, frozen manifest hash, asset hashes, browser/version, device scale factor and final HTML hash in internal QA evidence.
12. Render at exact target dimensions and hand the result to `visual-quality-assurance`.
13. Run `scripts/validate_standalone_delivery.py` with the final HTML, frozen manifest and QA evidence. Deliver only if the gate passes.

## Reproducibility

Equivalent output requires the same validated manifest, same asset bytes, same compiler version, same fonts, and equivalent rendering environment. Browser font rasterization and platform differences can prevent byte-identical PNG output; define visual tolerances instead of claiming universal pixel identity.

## Repair policy

A correction updates only the defective layer or its dependencies. It must not regenerate or reposition unrelated layers. The end result should resemble a carefully organized visual design file expressed in HTML, not a responsive webpage or a flattened image wrapper. Any structural change creates a new manifest version and revalidates all dependent relationships.

## Output contract

The only customer-facing output is the final verified standalone HTML file. The layer manifest, assets, masks, source crops, compiler metadata and compile report are internal evidence and must not be attached or linked to the customer. The HTML must be self-contained, offline-capable and render at exact native artboard dimensions. If the verification gate fails, do not deliver the HTML candidate. See [layer manifest reference](references/LAYER-MANIFEST.md), `schemas/layer-manifest.schema.json` and `resources/FINAL-HTML-ONLY-DELIVERY.md`.

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.
