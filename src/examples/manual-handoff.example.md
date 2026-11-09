# Continue manually in ChatGPT

You are continuing an existing PixelPerfect Studio visual reconstruction job because one or more integrated services are unavailable.
Do not restart the project, ask me to repeat known requirements, or ask me to re-upload a file that is still accessible in this conversation.
Use the reference files already attached to this conversation and the checkpoint details below. If this is a new conversation and an input is marked `requires_reupload`, ask only for that specific missing file.

## Project
- Name: Campaign poster reconstruction
- Project ID: poster-demo-001
- Checkpoint ID: pp-demo-continuity-001
- Canvas: 1080 × 1350 px
- Current stage: `ASSET_READY`
- Completion status: `PARTIAL`
- User goal: Reconstruct the supplied poster at exact dimensions and deliver editable HTML/SVG plus a QA report.

## Source inputs
- `ref-001` (reference image): Original poster supplied in the current ChatGPT conversation. Availability: `available_in_current_chat`.

## Completed and pending stages
- `INTAKE`: **COMPLETED**. Goal, dimensions and deliverables confirmed
- `FORENSICS`: **COMPLETED**. Visual hierarchy, copy, palette and major geometry recorded
- `LAYER_PLAN`: **COMPLETED**. Layer manifest approved and versioned
- `ASSET_PLAN`: **COMPLETED**. Asset methods and provenance requirements recorded
- `ASSET_READY`: **BLOCKED**. Cloudinary transformation endpoint unavailable; continuing with original uploaded files Failure: Media transformation service timeout.
- `COMPILE`: **NOT_STARTED**. Awaiting asset substitutes or manual SVG construction

## Existing artifacts
- `reference-analysis.json` (analysis), availability: `downloadable`. Manually reviewed analysis; uncertain font IDs remain candidates
- `layer-manifest.json` (layer_manifest), availability: `downloadable`. Approved structural manifest

## Service failure and fallback
- Mode: `MANUAL_CHATGPT`
- Reason: Cloudinary media transformation endpoint timed out.
- Unavailable services: Cloudinary transformations
- Limitations: No automated Cloudinary transformations; Perceptual QA remains pending until a render can be produced and inspected

## Open items
- Confirm candidate typeface
- Render the HTML/SVG composition
- Run region-weighted visual QA

## Next action
Continue manual asset substitution and compile the composition in the current ChatGPT conversation.

## Instructions for this continuation
1. Continue the same job from the current stage and preserve all approved decisions and artifacts.
2. Use available ChatGPT vision, reasoning, file, Python, code, and artifact tools. Do not assume any external integration is available.
3. Produce the same requested deliverables wherever the current host can genuinely create them.
4. Never claim an upload, OCR run, segmentation, render, numerical metric, database write, cloud job, or Figma operation happened unless it actually did.
5. If rendering or numerical QA cannot run, deliver the editable source and mark those checks pending. Separate manual observations from measured results.
6. Continue through the remaining stages where possible. Do not stop at an error message or ask me to restart.
7. At the end, provide the completed work, residual limitations, and an updated continuity checkpoint with one next action.

This handoff contains checkpoint metadata only. Original images, fonts, and other source binaries must remain attached or be re-uploaded only when actually unavailable.
