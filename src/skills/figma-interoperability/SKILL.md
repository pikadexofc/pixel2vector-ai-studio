---
name: figma-interoperability
description: Use when transferring a reconstructed design, layer manifest, design tokens, or component system into Figma, or when validating an editable Figma representation against its source.
---

# Figma Interoperability
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Treat Figma as a separate editable representation of a validated design, not as an image-export destination. The source layer manifest and design tokens remain the canonical mapping input until a deliberate Figma ownership decision is made.

## Preconditions

Require a validated layer manifest, asset records, tokens, the target Figma file or explicit new-file request, and an available authorized Figma connector or import workflow. If the Figma tool is unavailable during a reconstruction task, preserve the mapping plan and export artefacts internally without claiming to modify a Figma file or delivering those artefacts separately.

## Mapping procedure

1. Read the layer manifest and identify which elements need to be editable as text, vector, shape, image, group, mask, or effect.
2. Map stable manifest IDs to Figma node IDs and persist the mapping as an export record. Do not use object names as the only identity key.
3. Translate design tokens into Figma variables/styles using the current Figma integration and design-token conventions. Preserve semantic token names and light/dark modes where defined.
4. Map parent/child hierarchy, x/y geometry, size, z-order, opacity, blend mode, corner radius, clipping, typography, and image crop. Record any unsupported or approximate property.
5. Preserve original source assets and upload/import only approved variants. Maintain asset provenance and licence metadata outside the Figma node where the platform cannot store it.
6. Use the actual Figma connector/import tool exposed in the host. Load its current skill/API guidance before any write operation.
7. Read back the created/updated file structure when the connector supports inspection. Compare node count, IDs, bounds, hierarchy, text content, token bindings, and image references with the source manifest.
8. Render/export a screenshot from Figma and run a visual QA comparison against the reference or deterministic compiler render.
9. Record a round-trip report with supported mappings, lossy mappings, unresolved differences, and connector/tool version.

## Critical limitations

- `html2canvas` produces a raster screenshot. It does not create an editable Figma layer tree.
- Importing SVG or HTML does not guarantee that every effect, font, mask, blend mode, or layout constraint becomes a native editable Figma property.
- Do not claim exact editability without inspecting the resulting Figma nodes.
- Do not make Figma file changes without explicit user authorization and a connected write-capable tool.

## Output

Provide a manifest-to-node mapping, token mapping, import/export result, validation evidence, and list of properties that were approximated or lost. A successful API call alone is not proof of visual parity.

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.


## PixelPerfect customer delivery boundary

For reconstruction jobs, preserve working tokens, mappings, source data, implementation files and validation evidence internally. The only default customer-facing deliverable is one final verified standalone HTML file. Do not attach previews, manifests, assets, reports, project folders or ZIP bundles. If the final HTML acceptance gate cannot pass, do not provide an unverified candidate.
