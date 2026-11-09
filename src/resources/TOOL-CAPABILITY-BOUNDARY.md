# Tool capability boundary

The plugin is skills-only. It contains no remote MCP server, credentials, hosted service, or custom UI.

Skills may guide use of host-native capabilities when exposed: image input, read/list/search/grep, write/patch, shell, Python, browser/search, image generation, Figma, and connected service tools. Their presence depends on the host, user plan, and current session.

External service status must be checked each task. Supabase, Cloudflare, GitHub, Notion, Figma, and AI provider access are not presumed configured by the architecture document. Do not create resources or mutate external state without explicit user authorization.

## Suggested implementation adapters (not bundled dependencies)

| Function | Candidate tools | Constraint
|---|---|---|
| Image metadata and orientation | Pillow, Sharp | Preserve originals and record transforms. |
| Image geometry and processing | OpenCV, scikit-image | Pin runtime versions after benchmark. |
| OCR | PaddleOCR, Tesseract, Google Cloud Vision | OCR text/boxes are observations, not exact typography identification. |
| Detection and segmentation | Grounding DINO, SAM-family models | Keep model/version and prompt; preserve masks. |
| Browser render | Playwright | Pin browser, viewport, fonts and device scale factor. |
| Pixel comparison | Pixelmatch, OpenCV | Separate per-pixel threshold from overall mismatch ratio. |
| Perceptual comparison | SSIM implementations | Complement, never replace, visual inspection. |
| Design tokens | W3C Design Tokens Community Group format | Use a documented version and semantic token names. |
| Figma | Connected Figma MCP/API/import workflow | Inspect and map actual nodes; screenshot import is not editable-layer export. |
| Memory | Supabase PostgreSQL, pgvector | Keep PostgreSQL authoritative initially. |
| Binary storage and durable jobs | Cloudflare R2, Workers, Queues, Workflows | Add each component only when implemented and configured. |

These are candidate adapters, not dependencies installed or configured by this plugin. Version compatibility must be checked against the current runtime before implementation.
