# Brand asset status

**Status:** user-supplied icon pack imported and inspected for PixelPerfect Studio 0.2.1.

The user supplied `pickko_plugin_icon_pack.zip`. The pack contains:

- `icon.svg`: 1024×1024 numeric SVG dimensions with a square viewBox.
- PNG exports at 16, 24, 32, 48, 64, 96, 128, 180, 192, 256, 512, and 1024 pixels.
- `favicon.ico`, an asset manifest, and source README.

The original pack is retained under `assets/icon-pack/`. The portable manifest uses the supplied 1024px PNG as `logo` and 128px PNG as `composerIcon`. Dark variants use the same supplied artwork because the icon is already designed as a dark purple/blue square; no altered alternate was invented. The earlier provisional SVG assets remain in `assets/` as supplementary brand assets, not as the declared primary icon.

Validation must check all PNG dimensions, square geometry, SVG XML parsing, manifest paths, archive inclusion, and image file limits. This records packaging evidence only, not an OpenAI directory approval.
