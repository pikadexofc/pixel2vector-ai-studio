# Install PixelPerfect Studio 1.0.0

## What you are installing

PixelPerfect Studio is a Skills-only Agent Plugin. Its purpose is simple: convert a flat image into a high-fidelity editable layered HTML design. The HTML is a fixed-size artboard, not a responsive website. The customer-facing reconstruction output is one verified standalone HTML file.

The portable plugin ZIP contains one top-level `pixelperfect-studio/` folder with the root `plugin.json`, the `.codex-plugin/plugin.json` compatibility manifest and eleven Skills. It contains no hosted MCP server or custom UI.

## Portable plugin ZIP

Use `PixelPerfect-Studio-Plugin-1.0.0.zip` with a host surface that supports portable plugin ZIP import. The archive structure has been validated to contain exactly one top-level plugin folder. Import availability differs by ChatGPT client and version; the actual ChatGPT UI import has not yet been independently smoke-tested for this release.

## First use

1. Start a new conversation with PixelPerfect Studio enabled.
2. Upload the original image at the highest available quality.
3. Send: **Convert this image into a high-fidelity editable layered HTML design. Preserve its original dimensions. Separate every meaningful component into its own layer, and extract or generate individual PNG assets wherever needed. Deliver only the final verified standalone HTML.**
4. Let the workflow inspect the image, map layers, recover typography, produce separate visual assets, build the fixed artboard, render and verify it.
5. Receive only the final verified standalone HTML file.

You do not need to prepare a manifest, split the image, find fonts, or write code. State only special constraints that are not visible in the reference.

## Optional Windows personal marketplace route

For ChatGPT desktop clients using the local personal plugin marketplace, build a Windows install bundle from the plugin source folder:

```bash
python3 scripts/build_local_marketplace.py . ../PixelPerfect-Studio-Local-Marketplace-1.0.0.zip
```

Extract that bundle on Windows, open PowerShell in the extracted folder and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\Install-PixelPerfectStudio.ps1
```

The installer backs up an existing PixelPerfect folder and preserves other entries in the personal marketplace. Restart ChatGPT desktop, open Plugins, choose the Personal marketplace, and install PixelPerfect Studio. This is a local desktop workflow; it cannot install into a remote/mobile ChatGPT session. Do not run the installer unless you intend to update the local desktop plugin.

## Codex compatibility

The `.codex-plugin/plugin.json` compatibility manifest is included. The package is skills-only. Client versions can differ in their import and discovery behavior; use the documentation for the exact host client being used. No remote MCP server or credentials are bundled.

## What installation does not do

Installation does not connect Supabase, Cloudflare, GitHub, Notion, Figma, image-generation providers or OCR services. It does not provision credentials, deploy a remote MCP server, grant filesystem access or publish to the public Plugin Directory. Skills guide the host agent to use capabilities that the active host actually exposes.
