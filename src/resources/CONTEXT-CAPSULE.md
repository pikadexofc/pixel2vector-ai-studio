# PixelPerfect Studio operational context capsule

## Mission

Convert a flat image into a high-fidelity, editable, fixed-size HTML design. Each meaningful component must remain independently addressable as an HTML/CSS, SVG or individually embedded PNG image layer. The HTML is a design document/artboard, not a responsive website. Extract source imagery first; generate separate PNG assets when extraction cannot meet quality. Deliver exactly one final verified standalone HTML file. Manifests, prompts, source/generated PNGs, assets, renders, metrics and QA evidence are internal production requirements, not customer deliverables.

## Core principle

Probabilistic intelligence may identify, estimate, rank, or recommend. The deterministic production path consumes reviewed and frozen inputs. QA independently evaluates the render. Knowledge promotion requires evidence.

## Key technical corrections

- Normalize EXIF orientation before coordinate measurement.
- Use top-left canvas origin and pixel coordinates. Represent boxes as `x_min/y_min/x_max/y_max`.
- OCR detects text and regions; it does not identify an exact font.
- Palette extractors identify prominent colours; they do not reconstruct gradient spatial geometry. Sample colours at coordinates.
- Segmentation masks are primary; bounding boxes derived from masks are secondary.
- Pixelmatch per-pixel threshold is different from whole-image mismatch ratio.
- `html2canvas` is not an editable Figma-layer exporter. Figma interoperability needs a separate layer/token mapping.
- Preserve source assets; do not overwrite originals with variants.
- Visual similarity is not a substitute for licence eligibility.

## Layer methods

For each meaningful component choose one primary method: `SOURCE`, `GENERATE`, `CODE`, `SVG`, or `TYPOGRAPHY`. Use ChatGPT image generation to create separate PNG assets when needed and available; never generate the full composition as a flattened implementation asset. Record why and the evidence supporting the choice.

## Customer output

Deliver exactly one final verified standalone `.html` file. Do not deliver previews, manifests, asset records, QA reports, difference maps, source folders or ZIP bundles. If the final acceptance gate cannot pass, deliver no HTML candidate and state the specific blocker.

## Internal production evidence

Maintain an exact-size render, frozen layer manifest, asset records/provenance, comparison metrics, environment metadata and QA evidence. Keep these internal and use them to authorize the single HTML deliverable.

## QA sequence

Three passes: structural integrity, visual fidelity, finishing. Fix specific defective layers; do not regenerate the whole composition to solve one local defect. Do not claim pixel-perfect without actual render and inspection.

## Persistent architecture selection

Supabase PostgreSQL owns structured metadata and graph relationships. pgvector is the initial primary semantic index. Cloudflare R2 owns binary assets. GitHub owns source, schemas and version history. Notion provides human-facing knowledge views. Cloudflare Workers/Queues/Workflows are staged as required. D1 and a separate graph DB are not selected for MVP.

## Trust lifecycle

`NEW`, `TESTED`, `VERIFIED`, `CANONICAL`. Agents may propose; they may not silently promote to canonical. Retain evidence, provenance, version, source, licence, and QA context.

## Relevant aesthetic context

Use clean, minimal, high-contrast composition. Dark/charcoal, soft white, and selective cyan/chromatic accents are common preferences. Avoid noisy, cartoonish, gratuitously cyberpunk/neon, graffiti, and heavy-texture solutions. The Editorial Neo-Brutalist Collage v1.1.0 modes are conditional and activate only when explicitly requested.

## Exclusions

Do not package raw private conversation logs, sensitive personal context, credentials, client-confidential assets, or private source code from unrelated repositories. This plugin preserves operational design and engineering knowledge only.


## Manual continuity invariant

A service outage must not end the customer's design job. If ChatGPT remains available, continue manually in the current conversation using accessible references and host tools. Preserve completed outputs, mark unavailable automation and metrics, and save a continuity checkpoint. If ChatGPT itself is unavailable, retain local internal project files and a private checkpoint for later resumption. Never expose recovery files as reconstruction deliverables. Never put secrets or binary file contents in checkpoints.
