# Final HTML-Only Delivery Contract

**Version:** 1.0.0  
**Status:** Mandatory product contract  
**Applies to:** Every PixelPerfect Studio reconstruction job and every customer-facing host surface.

## North star

The customer receives exactly one deliverable: **the final, verified, standalone HTML file**.

All other project artifacts are internal production evidence. They are not customer deliverables by default.

## Customer-facing output policy

- Deliver one `.html` file only.
- Do not attach or link previews, screenshots, reference crops, extracted assets, generated assets, font files, manifests, asset registers, analysis JSON, QA reports, difference maps, source folders, ZIP archives, project bundles, READMEs, or continuity checkpoints.
- Do not describe internal evidence files as optional downloads. They are not part of the default customer handoff.
- Do not send a draft, first-pass render, approximate version, or unverified HTML file as the final result.
- If the final acceptance gate fails or cannot be run, do not deliver an HTML candidate. State the specific blocker in concise prose and preserve the work internally for continuation.
- Progress updates may describe the current stage or a blocker, but must not expose intermediate artifacts or turn them into deliverables.
- Do not make the customer choose among internal production formats. The reconstruction handoff is the standalone HTML.

This contract controls reconstruction delivery. Internal manifests, assets, renders, QA records, source code, and evidence remain necessary to produce and verify the HTML, but they are not the final user-facing output.

## Standalone HTML requirements

The final HTML must:

1. Be a complete UTF-8 HTML5 document.
2. Contain all required images, textures, SVG, CSS, scripts and fonts inside the file as embedded data or inline content.
3. Have no external runtime dependencies, relative asset paths, CDN links, remote fonts, remote stylesheets, or network calls.
4. Preserve the exact native reference artboard dimensions and top-left coordinate system.
5. Preserve independent layer identity in the DOM using stable `data-layer` identifiers.
6. Match the frozen manifest's layer ID set exactly.
7. Have no missing assets, broken fonts, critical text mismatch, canvas overflow, or browser console errors.
8. Open and render offline in the recorded browser environment.

Hyperlinks that are part of the design may remain navigational links. They must not be required to load the composition.

## Required internal acceptance gate

Before delivery, all requirements below must pass:

### A. Source and artboard
- Original input is preserved and SHA-256 recorded.
- Detected media format is derived from file bytes, separately from the supplied filename extension.
- Normalized source dimensions, orientation and crop are recorded.
- Render dimensions equal the source artboard exactly. Do not rescale a mismatch away.

### B. Frozen layer and asset integrity
- Layer manifest is frozen and contains unique stable IDs.
- Every manifest ID maps to exactly one HTML `data-layer` ID.
- Every layer asset reference resolves to a stable asset record and matching SHA-256.
- Layer geometry, z-order, clipping, masks and intentional bleed are explicit.
- Browser-computed bounds and z-index are recorded for every layer and compared against the frozen manifest; no missing or extra layer records are allowed.
- Documentation counts are generated from the manifest, never maintained manually.

### C. Standalone runtime
- All runtime resources are embedded.
- No external or relative runtime references remain.
- Fonts and images load successfully in the actual render environment.
- Browser console error count and runtime network request count are zero.
- Every manifest asset and required font has an explicit successful browser load check.
- Every semantic TYPOGRAPHY layer has exact rendered-copy verification against its frozen manifest content.
- Canvas overflow and critical text clipping are absent.

### D. Three review passes
- Structural: exact dimensions, layer completeness, geometry, stacking, clipping, asset/font loading and boundaries.
- Fidelity: typography/glyph shape, source crops, masks, colour, texture, gradients, contrast, spacing and key imagery.
- Finishing: antialiasing, edge quality, small alignment, distress details, legibility and final composition.

### E. Quantitative comparison
- Reference and render are compared at identical dimensions, crop, orientation and colour-space policy.
- Record the algorithm and version, preprocessing, per-pixel colour threshold, mismatch ratio, MAE and SSIM separately.
- Add region-level checks for critical text, logos and major visual subjects.
- When a validated benchmark or user-approved project profile exists, apply it and require all measured values to satisfy it.
- When no calibrated profile exists, mark numerical metrics `diagnostic_only`; bind a direct three-pass visual review to the exact reference and render SHA-256 hashes, and identify the critical regions reviewed. Never invent universal thresholds or present diagnostic values as objective pass/fail truth.
- In either mode, hard structural/runtime checks and the three visual QA passes remain mandatory.

### F. Defect status
- No open or deferred defects remain.
- Any accepted non-critical defect needs an explicit approver and reason and must remain within the approved profile.
- Critical text, logo, major geometry, broken asset and canvas defects must be fixed, not waived.

### G. Hash binding
- The QA record contains the final HTML SHA-256.
- The validator recomputes and matches that exact hash after all edits.
- Any edit after QA invalidates the previous approval and requires rerendering and revalidation.

## Status vocabulary

`RENDERED` → `STRUCTURALLY_VALID` → `VISUALLY_REVIEWED` → `QUANTITATIVELY_EVALUATED` → `FIDELITY_ACCEPTED` → `DELIVERABLE_VERIFIED`.

Only `DELIVERABLE_VERIFIED` permits delivery.

`PIXEL_IDENTICAL` is a separate claim and may be used only when exact pixel equality has been demonstrated. A verified deliverable does not automatically mean pixel-identical.

## Failure behaviour

If an automation or service fails, use the best available manual route. Preserve the job, known context, approved decisions and internal evidence. The final output policy does not change: never send an unverified HTML candidate or a collection of intermediate files as a substitute.

If rendering, comparison, font loading, asset loading, or another required acceptance check cannot be performed, mark delivery blocked and explain the exact missing verification. Do not fabricate evidence or claim completion.

## Independent design-layer fidelity

The artboard must represent the visual reference as a structured design, not as a screenshot wrapped in HTML.

- Every meaningful visual component must have one stable, independently addressable `data-layer` identity.
- Separate photographic or illustrative assets remain separate image elements. Each required PNG is embedded individually in the standalone HTML.
- Source-derived crops/masks and generated PNGs are internal asset inputs; they are not flattened together before HTML assembly.
- Layer groups may express logical parent-child structure, but a group must not hide components that should be separately editable.
- Do not over-fragment the artwork into meaningless pixels or excessive trivial DOM nodes. A layer represents a meaningful design component a designer could reasonably select, move, replace, hide or edit independently.
- The design is fixed-size and non-responsive. Do not add mobile reflow, responsive breakpoints or website/application behavior unless the user explicitly changes the task.
- Do not sacrifice image quality through aggressive downscaling or lossy recompression merely to reduce the HTML file size.
