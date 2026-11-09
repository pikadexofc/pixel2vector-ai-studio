# Asset provenance and rights reference

## Source hierarchy

1. User-provided original asset with explicit project permission.
2. Official brand/product repository or asset library with documented terms.
3. Public asset repository with a verified licence attached to the exact asset.
4. Paid/stock source with a recorded entitlement and permitted use.
5. Generated asset when generation is appropriate and the output is reviewed.

## Provenance fields

Record stable asset ID, file hash, perceptual hash, MIME type, dimensions, colour mode, transparency, filename, source URL/provider, author/creator, licence identifier and URL, attribution text, retrieval date, permitted actions, usage restrictions, project/layer IDs, processing history, generation prompt/model, parent version, and review state.

## Rights states

- `verified`: licence/permission reviewed for the intended use.
- `restricted`: usable only under recorded conditions.
- `unknown`: terms could not be verified.
- `prohibited`: intended use conflicts with rights/terms.

Only `verified` or a reviewed `restricted` asset may be used for an output. Unknown does not mean free to use.

## Immutable storage

Original bytes are immutable. Every crop, resize, retouch, mask, compression, or recolour creates a new variant and links to the source. A new asset with identical bytes may reuse the existing content-addressed object but must retain its project/layer provenance edges.

## Duplicate resolution

Cryptographic hash detects byte-identical files. Perceptual hash helps identify visually similar variants but is not proof of identity or licence. Embedding similarity is a retrieval aid, not a duplicate decision by itself.

## Generation records

Record the actual tool/model identifier only when known, prompt, settings, seed if provided, timestamp, input reference IDs, edit history, and inspection outcome. Do not invent a seed or claim a deterministic result from a stochastic generator.


## Source-derived visual elements

When an asset is extracted from a supplied reference, retain the parent reference SHA-256, exact source bounding box in normalized reference pixels, mask method, mask revision, antialiasing scale, edge feathering, crop/transform history and final asset SHA-256. The untouched original remains immutable. A source-derived raster/SVG glyph asset is artwork, not a recovered typeface file.

Prefer extracting a recognizable source element over generating a replacement when the source pixels can be isolated cleanly. Generate only when the source is occluded, inseparable, too small, or fails native-size inspection. Record the reason for any generation replacement.
