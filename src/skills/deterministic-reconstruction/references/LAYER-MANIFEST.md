# Layer manifest reference

The canonical machine-readable contract lives at `schemas/layer-manifest.schema.json`. The manifest is the authoritative ordered map from visual design elements to compiled layers.

## Required concepts

- `schema_version`, `manifest_id`, `project_id`, the complete `source` record, `canvas`, `coordinate_system`, `layers`, `assets`, `provenance`, and `version`.
- The source record separates the filename supplied by the user, byte-detected format, raw stored dimensions, EXIF-normalized dimensions, byte size, SHA-256, mode, EXIF orientation and ICC profile hash. The normalized dimensions must equal the artboard.
- Every layer has a stable unique ID, name, type, geometry, z-index, visibility, opacity, blend mode, and production method.
- Optional data includes group/parent, transform, crop, clipping, mask, shadows, gradients, typography, content, asset references, source-region evidence, confidence, and notes.
- Source-derived assets record parent source hash, source bounding box, mask method, antialiasing/feathering and output hash.
- Text layers record typography recovery mode: exact verified font, extracted source glyph raster, extracted SVG glyph paths, approved substitute or unknown. Extracted glyph artwork is never labelled as a recovered font file.

## Coordinate example

```json
{
  "x_min": 120,
  "y_min": 80,
  "x_max": 620,
  "y_max": 280
}
```

The width is 500 px and height is 200 px. Do not store contradictory width/height values unless they are explicitly declared as cached derived values.

## Freeze rule

A reviewed manifest becomes `frozen` before asset finalization. Any change to canvas, layer identity, geometry, order, or production method creates a new manifest version and invalidates dependent compile/QA results. Cosmetic asset changes require at least a new asset version and a new compile.


## Typography recovery record

Identify the exact font and compare its rendered glyph shapes first. When the exact font is unavailable or the glyphs do not match, record source-derived glyph artwork in the layer. Prefer SVG paths where vectorization preserves the shape; otherwise use transparent raster glyphs. Keep the semantic text separately. Preserve word width, glyph proportions, kerning, tracking, baseline, line breaks, slant and source distress. A substitute font is not an exact match.

## Source file byte truth

The supplied filename extension is not proof of file format. Record the format decoded from the file bytes. Preserve raw dimensions and normalized dimensions independently when EXIF orientation changes the image axes.
