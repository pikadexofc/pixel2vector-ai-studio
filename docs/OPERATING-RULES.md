# PixelPerfect Studio Operating Rules

**Status:** Proposed mandatory rules for the next plugin revision. Documented here first; not yet integrated into plugin code.

## A. Intake and source preservation

1. Preserve the original input; never overwrite it.
2. Record supplied filename, detected format from file bytes, dimensions, mode, orientation, byte size and SHA-256.
3. Use a top-left origin and pixel coordinates relative to the exact native artboard.
4. Record observations as `OBSERVED`, `DERIVED`, `ESTIMATED` or `UNKNOWN`, with evidence and confidence.
5. OCR text recognition does not establish font identity.

## B. Layer contract

Every layer must have:

- Stable unique ID and descriptive name.
- Group, parent/child and occlusion relationships where needed.
- `x`, `y`, `width`, `height` or an explicit vector/path/mask definition.
- `z_index`, opacity, transforms, clipping and blend settings where applicable.
- One declared primary production method: `SOURCE`, `GENERATE`, `CODE`, `SVG` or `TYPOGRAPHY`.
- Confidence, evidence, dependencies and QA state.

The manifest is the source of truth. HTML/SVG implementation, asset register, README counts and stage ledger must agree with it.

## C. Asset method decision tree

1. Can the element be isolated from the supplied reference with acceptable quality? Use `SOURCE` with an extraction/mask record.
2. Is it deterministic geometry or simple repeatable structure? Use `CODE` or `SVG`.
3. Is it typography? Identify the font and compare rendered glyphs. If the font cannot be found or is visibly wrong, extract letterforms from the reference and preserve them as source-derived artwork.
4. Is it a photographic subject that cannot be adequately extracted? Use `GENERATE` as an independent asset, not a flattened full design.
5. Record provenance, source bounds or generation prompt, rights status, hashes and contextual QA.

## D. Typography recovery rule

Exact font search comes before substitution. If unavailable, extract the visible letterforms from the reference. Clean and vectorize glyphs where practical; preserve original width, height, slant, tracking, kerning and line breaks. Keep texture/distress as separate overlays when possible. Never claim an original font file was recovered when only its raster letterforms were recreated.

## E. Compilation and rendering

1. Compile against a fixed-size artboard matching the source dimensions.
2. Use explicitly scoped CSS; do not let broad shared selectors override layer coordinates.
3. Emit explicit z-index and geometry from the manifest.
4. Embed or package all assets locally when offline output is required.
5. Render at exact target dimensions and record browser, version, viewport, device scale factor, fonts and asset set.
6. Responsive scaling is not equivalent to an independently art-directed mobile composition.

## F. QA gates

### Pass 1: Structure

Canvas dimensions, layer completeness, manifest/HTML ID equality, geometry, z-order, clipping, overflow, loaded assets, font loading, console errors and boundary containment.

### Pass 2: Styling

Typography/glyph shape, colour, crops, texture, gradients, contrast, spacing, shadows, blend modes and source-mask quality.

### Pass 3: Fidelity and finish

Small alignment, edge precision, antialiasing, distressed texture, critical text/logo match, regional defects and delivery completeness.

### Numerical comparison

At matched dimensions and crop, produce raw difference and threshold maps. Report the per-pixel colour-distance threshold separately from mismatch ratio. Report MAE and SSIM as diagnostics. Add region-level comparisons for critical text, logo and key image regions. Record algorithm/version and preprocessing parameters.

## G. Status vocabulary

`RENDERED` → `STRUCTURALLY_VALID` → `VISUALLY_REVIEWED` → `QUANTITATIVELY_EVALUATED` → `FIDELITY_ACCEPTED`.

`PIXEL_IDENTICAL` is allowed only after exact pixel equality is demonstrated. A successful build, zero console errors or a high similarity metric does not independently justify that label.

## H. Release consistency

- Derive layer counts from the manifest.
- Compare the unique manifest ID set with the unique HTML ID set.
- Verify every asset reference resolves and every local asset hash matches its record.
- Validate the archive opens and contains the expected project files.
- Keep all known defects and unverified claims visible in the final QA report.
