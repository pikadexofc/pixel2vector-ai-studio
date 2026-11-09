# PixelPerfect Studio: Learnings and Fixes

**Archive version:** 1.0  
**Record date:** 2026-11-03  
**Projects reviewed:** Legal Systems cover workflow, SubPilot poster, After the Noise banner  
**Status:** Documented; plugin integration not yet performed.

## 1. Executive finding

The three exercises establish a workable reconstruction pipeline, but they do not establish a universally reliable pixel-perfect system. The strongest evidence supports a layered, fixed-artboard, offline-capable HTML workflow with per-layer production methods, asset provenance, a synchronized manifest, and staged visual QA.

The key change in approach is to move from **approximating a flattened image** toward **recovering source evidence and rebuilding it as independently addressable components**. Use the supplied reference itself whenever a visual component can be isolated cleanly. Generate a replacement only when extraction is impossible, incomplete, or unsuitable. Treat typography as a first-class visual asset: identify the font first, then recover letterforms from the raster when necessary.

A successful render proves that the composition compiled. It does not prove that the composition is faithful.

## 2. Evidence summary

### 2.1 Legal Systems in Transition cover workflow

**Evidence class:** SOURCE_RECORDED. The uploaded `pixelperfect-workflow.json` records a complete workflow for a 1536 × 864 fixed artboard.

Recorded outcomes:

- 35 independently addressable layers with absolute geometry, groups, production method and z-order metadata.
- Separate production methods for generated photographic subjects, CSS/code geometry, SVG vectors and live typography.
- Selected image assets and font files embedded into a standalone HTML document.
- Three generated photographic/image subjects retained as individual assets; flattened full-poster generations were rejected for implementation.
- Four font data URIs and three image data URIs embedded in the final HTML.
- No external runtime dependencies and no JavaScript requirement.
- The record reports exact equality between 35 manifest IDs and 35 HTML `data-layer` IDs.
- Three visual review passes were recorded: structure, styling, and fidelity/finishing.

Important limitation: the workflow record explicitly says that no numerical SSIM, MAE or pixel-difference score was calculated. Its three QA passes were screenshot-based visual reviews. This is useful evidence of a process, not evidence of numerical similarity or pixel identity.

### 2.2 SubPilot poster

**Evidence class:** ARTIFACT_VERIFIED from `analysis.json`, `layer-manifest.json`, `qa-report.json`, `asset-register.json` and the rendered project files.

- Source canvas: 1536 × 1536, RGB JPEG.
- Manifest: 22 layer records.
- Render: 1536 × 1536 PNG using Chromium/Playwright.
- Three viewport sizes were checked: 1536 × 1536, 768 × 768 and 390 × 390.
- The QA report records no browser console errors and no clipping of the main headline, button or QR frame at the target canvas size.
- The QR image was retained as a source crop. The image-load test passed, but its payload was not decoded.
- The QA report records no numerical SSIM, LPIPS or pixel-mismatch comparison.

Documented unresolved defects:

- Exact display and logo font identities remain unknown.
- Paper grain, headline distress and halftone are procedural approximations, not source-recovered masks.
- The logo is editable typography, not the original vector wordmark.
- The player illustration and speech-bubble paths were reconstructed rather than traced from the source.
- The QR destination is unverified.

Interactive correction notes from the build:

- The first render had headline overflow and the player expression read incorrectly. These were corrected in subsequent local render iterations; the final QA artifact confirms headline containment, but it still records the illustration paths as reconstructed rather than source-traced.
- A coordinate review found the lower section and brand lockup misplaced. Their positions were corrected against source crops and rendered bounds.
- The final artifact remains explicitly `FIRST_PASS_RENDERED_NOT_PIXEL_VERIFIED`; it is not a certified exact reconstruction.

### 2.3 After the Noise banner

**Evidence class:** ARTIFACT_VERIFIED from `analysis.json`, `asset-register.json`, `layer-manifest.json`, `qa-report.json`, `stage-ledger.json` and `after_noise_build_log.json`.

- Source file was named `1000154722.png`, but the decoded file format is JPEG. Actual source canvas: 1536 × 569, RGB.
- The source SHA-256 recorded in the analysis is `1d9b0fda4d1c6972c7718574d40a891347c255d3d294d486cf75dedcc79a3a5c`.
- Manifest: 16 layer records.
- Asset register: nine source-derived transparent PNG cutouts, each with source bounding box, transform description, output hash and render validation.
- Render: 1536 × 569, Chromium via Playwright; the QA report records dimension match.
- All nine image assets were recorded as decoded and rendered.
- The responsive smoke test at 390 px reported no horizontal overflow. This is CSS scaling of the same artboard, not a separately composed mobile layout.
- Headline containment and layer separation checks passed.

Numerical comparison recorded in the QA report:

- RGB Euclidean pixel threshold: 24.
- Pixel mismatch ratio: 0.1672021456, approximately 16.72%.
- Mean absolute RGB error: 24.8132362.
- SSIM: 0.7280747.

These are diagnostic values for this particular reference/render pair and comparison setup. They are not universal acceptance thresholds. The QA report marks perceptual comparison as `REVIEW` and explicitly rejects a pixel-perfect claim.

Documented unresolved limitations:

- Headline font is approximate.
- Some architectural masks are hand-traced and may need edge refinement.
- Fine technical textures are approximated with SVG noise and vector marks.
- No alternate mobile composition is included.

The README says the manifest has 14 layers, while the actual manifest and stage ledger list 16 stable layer IDs. The manifest count of 16 is the authoritative artifact value for this build. The documentation mismatch is a defect and must be prevented by generated documentation or automated cross-checks.

## 3. Cross-project learnings

### L-001. Keep a fixed artboard as the geometric source of truth

All three workflows use a fixed canvas and top-left coordinate origin. The reconstruction target must retain the exact original width, height, orientation and coordinate space. Every layer should carry an explicit bounding box and z-order. Responsive scaling can be a presentation mode, but it must not silently change the native artboard or reflow the composition.

### L-002. A layer manifest is a real contract, not an optional description

The legal-cover workflow's 35-to-35 ID equality check is a strong model. Every manifest layer must resolve to exactly one intended HTML/SVG layer, unless a documented composite relationship is explicitly allowed. The manifest should record stable ID, name, group, geometry, z-index, opacity, transform, clipping/mask, production method, asset references and confidence.

### L-003. Choose a production method for each layer

The tested method vocabulary is `SOURCE`, `GENERATE`, `CODE`, `SVG` and `TYPOGRAPHY`.

- `SOURCE`: isolate, crop or mask an element from the supplied reference or an approved external source. Preserve provenance and parent-source coordinates.
- `GENERATE`: create an independent visual subject where the reference does not contain a clean reusable asset or extraction cannot meet the target.
- `CODE`: use deterministic HTML/CSS for blocks, layout, panels, simple shapes and repeatable geometry.
- `SVG`: use vector paths for technical lines, geometric accents, icons, masks and traced contours.
- `TYPOGRAPHY`: use live text only when the font and letterform approximation satisfy the brief. When exact letter shapes matter and the exact font cannot be found, use source-derived glyph artwork or SVG paths instead of a visibly wrong substitute.

Do not use a full-composition image generation as the final implementation when independent layers and editability are required. It may be used for visual exploration, but the final design should be reconstructed from separate components.

### L-004. Extract source imagery before generating replacements

After the Noise demonstrated that concrete beams, pillars, arch, staircase and torn paper could be isolated from the supplied image using polygon alpha masks. Nine source-derived fragments preserved image-specific texture and lighting better than newly generated generic architecture would.

The preferred order for a reference reconstruction is:

1. Inspect whether the element can be isolated from the supplied raster.
2. Extract it with a mask, crop and alpha edge treatment.
3. Inspect the extracted asset in context at native size.
4. Generate a replacement only if the source element is occluded, inseparable, too low-resolution, or visibly unsuitable.
5. Record which parts are source-derived and which are generated.

This is especially important for architecture, photographic textures, torn paper and distinctive hand-made illustrations.

### L-005. Typography recovery must precede font substitution

The user established this rule during the After the Noise test: search for the exact font first; if it cannot be found, extract the letterforms from the image. This is a mandatory product requirement.

Typography procedure:

1. Preserve the text content and measure each text region, line, baseline, width, height, tracking and alignment.
2. Inspect letterform characteristics and test plausible fonts at the target size.
3. Compare the rendered candidate with the reference, not merely the font name.
4. If the font is unavailable or still visibly wrong, isolate the headline glyphs or complete words from the source raster.
5. Clean masks, separate distress/halftone overlays from the glyph body where feasible, and trace to SVG paths when a clean vector result is practical.
6. Preserve the original glyph spacing and line geometry. Store the extracted glyph artwork as source-derived assets with hashes and source coordinates.
7. Use live editable text for supporting copy when it is not visually distinctive or when editability is the higher priority.

Do not claim to have recovered the original font file when only the visible letterforms were extracted. Do not redistribute an embedded font unless its licence permits it.

### L-006. Texture needs evidence, not just a filter

Procedural grain, halftone and distress are useful as a first pass, but SubPilot shows they remain a visible approximation when the source texture is distinctive. Extract source texture masks or preserve textured source regions when possible. Separate texture layers from type and geometry so they can be tuned independently.

### L-007. CSS scoping and explicit z-order prevent structural regressions

The After the Noise build exposed a headline-placement error caused by a shared CSS positioning rule overriding intended coordinates. It also exposed stacking mistakes between violet blocks, the torn black field and concrete structures.

Required fix pattern:

- Scope layout rules to the artboard and layer classes; avoid broad selectors that unintentionally affect every element.
- Define each layer's position and z-index explicitly in the manifest and compiler output.
- Use documented z-index bands for background, source imagery, structural geometry, foreground, typography and technical overlays.
- Validate the rendered bounding boxes against manifest boxes after compilation.
- Add a z-order regression test for overlapping critical layers.

### L-008. Treat extracted masks as assets, with edge QA

Polygon masks must be antialiased and reviewed at the final display size. The After the Noise asset register records 3× antialiasing, reduction and 0.5 px mask feathering. Preserve the original source bounding box, mask, output dimensions and hash. Inspect for halos, clipped concrete edges, transparent gaps and inconsistent feathering.

### L-009. Separate render success from visual-fidelity success

The three projects demonstrate three distinct levels:

- Build/render: HTML compiles and a preview is produced.
- Structural QA: canvas dimensions, layer mapping, asset loading, boundaries and console checks pass.
- Fidelity QA: text, geometry, texture, source image detail and perceptual difference have been reviewed and measured.

Only the third level can support a fidelity claim. A render is not `verified` merely because it exists or fits the canvas.

### L-010. Combine three visual passes with numerical comparison

Keep the three review passes used in the legal-cover workflow and SubPilot, then add the numerical method evidenced by After the Noise:

- Pass 1, structure: dimensions, geometry, missing layers, layer order, clipping, overlap, asset load, font load and boundary checks.
- Pass 2, styling: font/letterform match, colour, crop, texture, gradients, contrast, shadows and spacing.
- Pass 3, fidelity/finishing: edge quality, antialiasing, small alignment, texture detail, legibility and delivery completeness.
- Numerical comparison: raw difference map, thresholded difference map, mismatch ratio, MAE and SSIM; use region-weighted scores for critical areas such as headline or logo.

Always record the colour-distance threshold and mismatch ratio separately. SSIM and MAE are diagnostics; neither is a universal quality score by itself. Record metric implementation/version and exact comparison preprocessing.

### L-011. Use the asset register as a traceability layer

Every source-derived or generated asset should record stable ID, parent project/reference, source hash, source bounding box or prompt, transformation, output dimensions, output hash, rights status, QA state and dependent layer IDs. Original inputs remain immutable; variants are separate records.

### L-012. Keep the final HTML offline-capable when requested

The legal-cover workflow successfully embedded images and fonts as data URIs and recorded zero external runtime dependencies. Keep this capability. Validate that every required asset is embedded or packaged locally. No remote font/image/CDN dependency should be silently introduced into an offline delivery.

### L-013. Validate source file metadata from bytes

The After the Noise input had a `.png` filename but decoded as JPEG. Record both the supplied filename and detected file format. Do not trust the extension for decoding, metadata or reporting. Hash the original bytes before transformation.

### L-014. Generate counts and documentation from canonical structured data

The 14-versus-16 layer inconsistency is a preventable defect. Counts in README, stage ledger, manifest and HTML must be derived from the same manifest. A validator should compare the unique manifest IDs with the unique HTML layer IDs and fail delivery on unexplained differences.

### L-015. Keep QA evidence honest and reproducible

The legal-cover workflow reports three visual review passes but no numerical similarity. SubPilot reports responsive checks but no full-frame metrics. After the Noise includes actual metric values and labels them diagnostic. Preserve these distinctions. Every QA claim must point to an image, browser measurement, console log, comparison report or validator output.

## 4. Corrections observed and their status

| Defect | Project | Correction observed | Remaining work |
|---|---|---|---|
| Headline overflow | SubPilot | Coordinates and text sizing were revised; QA confirms headline containment | Exact typography/distress still unresolved |
| Incorrect player expression | SubPilot | Illustration was revised to read as a frown | Paths are still reconstructed, not source-traced |
| Lower panel and brand lockup misalignment | SubPilot | Geometry was revised against source crops | Fine details not numerically compared |
| Shared CSS rule overrode headline placement | After the Noise | CSS/layout was corrected in the build iteration | Add a permanent regression test and scoped-style rule |
| Wrong z-order of violet, torn field and structures | After the Noise | Stacking order was revised | Encode and validate z-index bands in the plugin/manifest |
| Missing edge detail / concrete upright | After the Noise | Top-left/bottom paper tears and right-side upright were extracted as source assets | Continue mask edge QA and quantify regional mismatch |
| Approximate typeface | Both posters | Identified as unresolved; user prescribed font search then source glyph extraction | Implement font identification and glyph extraction workflow |
| README says 14 layers, manifest has 16 | After the Noise | Discrepancy identified during audit | Generate documentation counts from manifest and add a validator |
| Input filename extension differs from decoded format | After the Noise | Correct format identified as JPEG | Add byte-signature format validation to intake |

**Important:** These are project-level corrections or documented recommendations. They have not yet been integrated into the PixelPerfect Studio plugin package. No plugin release has been modified by this archive operation.

## 5. Updated acceptance gates

A reconstruction may be labelled:

- `RENDERED`: exact-size render exists.
- `STRUCTURALLY_VALID`: canvas, required layers, asset loading, manifest mapping and boundary checks pass.
- `VISUALLY_REVIEWED`: all three visual review passes are recorded, with unresolved defects listed.
- `QUANTITATIVELY_EVALUATED`: difference maps and named metrics are produced at matched dimensions with settings recorded.
- `FIDELITY_ACCEPTED`: region-specific critical defects are resolved or explicitly approved against documented tolerances.
- `PIXEL_IDENTICAL`: only use when exact pixel equality has actually been demonstrated. This is not the same as a high SSIM score.

Do not collapse these statuses into a single green success state.

## 6. Priority fixes for the next implementation revision

### P0: Required before next serious reconstruction test

1. Font-first typography pipeline with glyph extraction fallback.
2. Source-image extraction/masking before generating replacement architectural or textural elements.
3. Explicit per-layer geometry and z-index contract.
4. Scoped CSS and manifest-to-render bounding-box validator.
5. Manifest/HTML ID set equality and documentation count validator.
6. Exact-canvas render and numerical QA report with threshold settings.

### P1: Required for repeatability and higher fidelity

1. Asset provenance, parent-source coordinates, output hashes and alpha-edge QA.
2. Region-weighted comparison for headline, logo, key imagery and architectural silhouettes.
3. Automated file signature detection independent of filename extension.
4. Typography/texture/source extraction uncertainty fields in the manifest.
5. A correction loop that repairs the smallest defective layer group and reruns only affected tests plus final full-frame QA.

### P2: Useful product improvements

1. Optional alternate mobile composition, separately approved from native fixed artboard output.
2. Learning capture for accepted masks, font/glyph methods, CSS fixes and QA failure patterns.
3. One-click export of HTML, manifest, asset register, preview, raw difference map, threshold map and QA report.

## 7. What this archive does not claim

- It does not claim that all three projects achieved pixel-perfect output.
- It does not claim that the legal-cover workflow's reported 35-layer equality or three QA passes were independently re-executed during this documentation task.
- It does not claim that SubPilot received numerical similarity evaluation.
- It does not claim that the After the Noise mismatch score is a universal pass/fail threshold.
- It does not claim that the font files or exact fonts were recovered for either poster.
- It does not change plugin code, skills, schemas, or packaging.

## 8. Next decision after documentation review

The next implementation step should be to update the plugin's forensic, asset-intelligence, reconstruction and QA skills and schemas using these rules, then run a controlled regression test on a new reference. The learning archive should remain the immutable v1.0 baseline for comparison.
