---
name: asset-intelligence
description: Use when extracting or generating separate PNG assets and other visual components for an editable layered HTML reconstruction.
---

# Asset Intelligence and Provenance
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Every asset must have a distinct visual role, associated layer ID, production method, provenance record, rights status, intended resolution and compatibility check. The objective is a high-quality editable design, not an optimized website. Visual similarity alone is not sufficient for reuse.

**Source-first rule:** for a reconstruction, first determine whether the visual element can be recovered from the supplied reference. Extract and mask source imagery before generating a replacement. Prefer source-derived architecture, paper tears, photographic textures, distinctive illustrations and other reference-specific visual material whenever clean extraction is possible. Generate only when extraction is occluded, inseparable, too low-resolution, or fails contextual quality review.

## Separate visual asset production

Use ChatGPT image generation as an actual production tool when an image asset is needed and the host exposes it. Generate each independent visual subject or asset role separately, normally as its own PNG, rather than generating the whole finished design. Prefer a transparent background for isolated foreground subjects when supported and appropriate. Generate separate variants for distinct assets; do not combine unrelated subjects in one output merely to reduce calls.

For every generated PNG:
- Match the reference's subject, camera angle, perspective, crop, lighting, colour, scale and visual role.
- Request adequate resolution for the intended on-canvas pixel size and avoid needless downscaling.
- Inspect the actual returned image, not only the prompt or tool status.
- Check transparent edges, halos, holes, shadows, unwanted scenery, extra objects, artifacts and crop safety.
- Reject or regenerate an asset that cannot meet the visual brief.
- Keep the PNG as a separate internal asset and embed it independently into its own HTML image layer.

If ImageGen is unavailable, use available source extraction or other authorized image tools. Do not claim a PNG was generated when only a prompt was written. Do not stop the job merely because one automation is unavailable; use the strongest available honest fallback and record the fidelity limitation.

## Choose a method per layer

Assign exactly one primary method to each layer:

- `SOURCE`: extract/crop/mask an element from the supplied reference, or source an approved existing asset. For reference-derived assets, record parent source hash, source bounding box, mask method, transforms, antialiasing/feathering and output hash. For external assets, record original URL/source, author, licence, retrieval date and permitted use.
- `GENERATE`: create a new, separate PNG visual asset when source assets cannot meet the brief or licensing constraints. Prefer one independent visual subject or asset role per generated image. Preserve the prompt, generator/model, parameters where available, generation time, source file hash and review result.
- `CODE`: construct with HTML/CSS/canvas or a deterministic program when the element is geometric, repeatable, or text-based.
- `SVG`: construct vector geometry or simple symbols that should remain crisp and editable.
- `TYPOGRAPHY`: identify and verify the exact font first. If it cannot be found or its rendered letterforms remain visibly wrong, extract the glyphs/words from the reference raster and preserve them as source-derived artwork. Vectorize to SVG paths where practical; use transparent source-glyph raster artwork when vectorization loses distinctive detail. Preserve semantic text/accessibility labels separately. Never call extracted glyph art a recovered font file.

The decision can be revised before freeze. After freeze, create a new asset version and update the manifest rather than silently overwriting an existing asset.

## Source workflow

1. Define the visual role and search terms from measured observations.
2. Search sources appropriate to the asset class and requested use. Candidate sources include Unsplash, Pexels, Openverse, Wikimedia Commons, Google Fonts, and official brand repositories such as Simple Icons or project-owned assets.
3. Prefer source-owner and licence documentation over aggregator summaries.
4. Verify candidate identity, crop, resolution, transparency, colour, and intended use.
5. Check licence compatibility for commercial use, modification, attribution, redistribution, and model training where relevant. Record unknown terms as `UNVERIFIED`; do not infer permission from public accessibility.
6. Save the original immutably. Store processed variants separately and link them to the original asset ID.
7. Generate content hashes and perceptual hashes; use embeddings only as an additional retrieval signal.
8. Inspect each asset independently and then in the complete artboard at native output size before marking it ready. For alpha masks, check halos, transparent gaps, clipped contours, edge feathering and antialiasing.
9. Prefer source extraction over GENERATE when both can meet quality requirements. Record why generation was necessary whenever a source element is replaced.

## Candidate ranking and rejection

Candidate ranking may combine visual similarity, graph relevance, context compatibility, verified quality, licence suitability, and provenance reliability. A previous starting hypothesis was `S = 0.30V + 0.20G + 0.20C + 0.15Q + 0.10L + 0.05P`; these weights are unvalidated and must be benchmarked. Licence incompatibility, missing provenance, unreadable resolution, and hard visual defects are rejection gates, not merely low ranking scores.

## Output contract

Create an asset record conforming to `schemas/asset-record.schema.json`. Include stable ID, original and variant hashes, dimensions, format, alpha/transparency, semantic description, source or generation record, project/layer references, licence, attribution, transformations, confidence, and validation state.

The final HTML must retain separate `<img>`/layer containers for distinct raster assets, with each asset embedded independently. Do not merge them into one flattened canvas screenshot. See [asset provenance reference](references/ASSET-PROVENANCE.md). Do not claim external assets were licensed or generated unless there is a supporting source or execution record. Keep asset registers, extracted crops, font files and provenance evidence internal; they are not customer deliverables. The customer receives only the final verified standalone HTML.

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.
