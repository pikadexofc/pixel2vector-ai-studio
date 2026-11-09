# PixelPerfect Studio

**Version:** 1.0.0  
**Publisher:** PixelPie Media  
**Purpose:** Turn a flat image into an editable, separately layered HTML design.

## What it does

Upload a poster, graphic, presentation cover, social creative, banner or other visual reference. PixelPerfect Studio studies the image, separates its meaningful components, recovers typography, extracts source details, and creates individual visual assets where needed. It then rebuilds the design on a fixed-size HTML artboard.

Each meaningful component remains independently identifiable as an HTML/CSS element, SVG layer or embedded image layer. Complex photographic subjects, textures and illustrations can be extracted from the reference or generated as separate PNG assets. Those assets are embedded individually into the final HTML so the file works offline.

**The HTML is an editable design canvas, not a responsive website.** The goal is visual quality and faithful reconstruction, not SEO, mobile reflow, application behavior, animation or website performance optimization.

## How to use it

1. Upload the original image at the highest available quality.
2. Send this instruction:

   **Convert this image into a high-fidelity editable layered HTML design. Preserve its original dimensions. Separate every meaningful component into its own layer, and extract or generate individual PNG assets wherever needed. Deliver only the final verified standalone HTML.**

3. PixelPerfect Studio performs the analysis, asset work, composition, rendering and quality review.
4. Receive one file: the final verified standalone `.html` design.

You do not need to prepare a layer manifest, write code, find fonts or split the image yourself. Ask only for a special constraint that is not visible in the reference, such as preserving editable text, retaining an exact logo, or avoiding generated replacements.

## What the result is

- One fixed-size artboard using the reference's normalized native dimensions by default.
- A structured HTML document with separate, named, independently addressable visual layers.
- Separate image assets embedded as individual image layers when raster artwork is the best visual method.
- Live HTML text when it matches the reference; source-derived SVG or transparent glyph artwork when the exact font cannot be recovered.
- Inline SVG and CSS for geometry, typography treatments, lines, borders, masks and effects where they offer better control.
- A single offline-capable HTML file containing everything needed to render the design.

## What it is not

- Not a responsive website builder.
- Not an app or interactive webpage generator.
- Not a single flattened screenshot placed inside an HTML wrapper.
- Not a promise of pixel identity. High fidelity must be demonstrated by the actual render and review.

## Delivery rule

The customer receives **only one final verified standalone HTML file**. Manifests, prompts, generated/source PNGs, crops, fonts, previews, difference maps, reports, checkpoints and project ZIPs are internal production evidence. If required verification cannot be completed or a critical defect remains, do not deliver an unverified HTML candidate; state the blocker briefly.

## Included

- Eleven specialist Skills for intake, visual forensics, asset production, reconstruction, QA, continuity and optional advanced workflows.
- The production workflow and evidence-backed learnings from three reconstruction exercises.
- Schemas and internal examples for analysis, layers, assets and quality evidence.
- Offline HTML acceptance validator, regression tests and deterministic plugin packaging scripts.
- PixelPie Media brand assets.

## Install and activate

Import `PixelPerfect-Studio-Plugin-1.0.0.zip` in a host surface that supports portable plugin ZIP import. The archive contains one top-level `pixelperfect-studio/` folder with both the portable and compatibility manifests.

After import, start a fresh conversation, attach a reference image and use the instruction above. Host import behavior varies; this package has been validated structurally, but actual ChatGPT UI import must be confirmed in the target client.

## Developer validation

From this directory:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s scripts/tests -v
python3 scripts/validate_plugin.py . --json
python3 scripts/validate_examples.py .
python3 scripts/package_plugin.py . ../PixelPerfect-Studio-Plugin-1.0.0.zip
```

For a reconstruction release, the internal delivery gate is:

```bash
python3 scripts/validate_standalone_delivery.py final.html layer-manifest.json qa-report.json reference.png render.png
```

The reference, render, manifest and QA record are internal gate inputs. They are not customer downloads. The delivery validator checks source-byte integrity, exact dimensions, layer IDs and geometry, asset/font loading, offline operation, text, numerical comparisons, visual-review records, defects and the final HTML hash.

## Honest capability boundary

This package is a Skills-based workflow and validation toolkit. Skills guide the host agent; they do not independently grant OCR, segmentation, image generation, a browser, file access, cloud services or connected accounts. Use the tools actually available in the host. Never claim an unavailable action was executed. If a required renderer or verification capability is unavailable, preserve the job and block final delivery rather than pretending it passed.
