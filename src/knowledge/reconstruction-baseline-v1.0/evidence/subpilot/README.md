# SubPilot poster reconstruction

Editable HTML/CSS/SVG reconstruction of the supplied 1536 × 1536 px poster.

## Open
Open `index.html` in a modern browser and keep the `assets` directory beside it. For a single-file option, open `SubPilot-Reconstruction-Standalone.html`; its QR crop is embedded. The artboard keeps a 1536 × 1536 coordinate system and scales to smaller viewports.

## Package contents
- `index.html`: editable HTML/CSS/SVG composition.
- `SubPilot-Reconstruction-Standalone.html`: one-file offline version.
- `preview.png`: exact 1536 × 1536 browser render.
- `layer-manifest.json`: reference-relative layer geometry and production methods.
- `analysis.json`: recognized text, palette estimates and unresolved evidence.
- `asset-register.json`: source and provenance record for the QR crop.
- `qa-report.json`: three-pass QA summary and known defects.
- `reference-original.jpg`: supplied source image for traceability.
- `assets/qr-reference.png`: source-preserving QR crop.

## Limitations
This is a rendered first pass, not a pixel-perfect certification. Exact font identities, the original vector wordmark, exact distress masks and QR destination remain unverified. No SSIM, LPIPS or pixel-mismatch score was measured. The QR crop is copied from the reference and its destination must not be assumed.
