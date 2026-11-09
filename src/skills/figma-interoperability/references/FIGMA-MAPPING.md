# Figma mapping reference

## Source of truth

The reviewed `layer-manifest.json` supplies geometry, hierarchy, z-order, visibility, opacity, blend mode, clipping, transforms, text and asset references. Design tokens supply semantic styles. Figma node IDs are a target mapping, not a replacement for stable source IDs.

## Property mapping

| Manifest concept | Figma target concept | Verification |
|---|---|---|
| Layer ID | plugin data or mapping table | ID uniqueness and round-trip lookup |
| Parent/group | frame/group hierarchy | parent IDs and nesting |
| Bounding box | x, y, width, height | pixel bounds within tolerance |
| Text content | text node | exact string and wrapping |
| Typography | text style/font properties | font available, size, weight, tracking, line height |
| Colour tokens | variables/styles | semantic binding, mode assignment |
| SVG/vector | vector or imported SVG | shape and bounds inspection |
| Raster image | image fill/node | crop, scale, source asset ID |
| Clip/mask | frame clip or mask node | rendered crop comparison |
| Shadow/effect | effect style | supported parameters and visual check |
| Opacity/blend | layer properties | exact property read-back where supported |

## Round-trip checks

Compare node counts, unique manifest IDs, text strings, geometry, hierarchy, token references, image hashes, and Figma export render. Classify each property as `exact`, `approximated`, `unsupported`, or `not-tested`.

## Permission boundary

A connected read capability does not imply write access. A Figma file key or URL does not itself authorize mutation. Use only tools and permissions that the current host exposes and the user has authorized.
