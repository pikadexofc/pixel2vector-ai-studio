---
name: manual-fallback-continuity
description: Use when a PixelPerfect Studio service, integration, model, renderer, storage layer, plugin action, or host tool is unavailable, failing, rate-limited, or too slow and the user still needs the visual design job completed.
---

# Manual Fallback Continuity
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Keep the customer's design task moving when integrated systems fail. The required behavior is graceful degradation, not a dead-end error message.

## Non-negotiable outcome

When a service fails but the current ChatGPT conversation remains available, continue the same job manually using the reference images, files, context, and host tools already available. User task completion comes first; usage metering is best-effort and must never block or interrupt an in-progress request. Do not make the user restart, repeat known requirements, or re-upload an attachment that is still accessible in the current conversation.

Complete every stage that available capabilities permit. Preserve the original goal and deliver the most complete truthful result possible. Never claim that a manual substitute ran an unavailable OCR engine, segmentation model, renderer, vector index, cloud workflow, or numerical QA tool.

## Activation signals

Activate this Skill when any dependency is unavailable, returns an error, times out, is rate-limited, loses authentication, exceeds a budget, or produces an unusable result. Also activate when a user asks to continue despite an outage.

## Recovery sequence

1. **Acknowledge the failure once.** Name the affected component and the effect on the current stage. Avoid stack traces and infrastructure jargon unless the user asks.
2. **Preserve state.** Reuse all accessible source attachments, the project brief, approved decisions, layer manifest, assets, renders, and previous QA findings.
3. **Classify the failure.** Distinguish transient outage, permission/authentication, quota/budget, invalid input, missing capability, and unavailable host. Retry only safe transient operations, with a bounded attempt. Do not repeatedly retry permission, quota, or invalid-input failures.
4. **Switch to manual ChatGPT mode.** Perform the remaining work in the current conversation using available vision, reasoning, file, Python, code, or artifact tools. Follow the same stage order and acceptance criteria as the automated path.
5. **Keep the same job moving internally.** Produce or update analysis, layer manifest, asset decisions, HTML/SVG, source code and QA evidence wherever the current host can actually produce them. Keep all intermediate artifacts internal.
6. **Mark residual limits.** State exactly what was completed manually, what remains unverified, and which automated measurements are unavailable. Manual continuation does not justify false fidelity claims.
7. **Create a continuity checkpoint.** Produce a portable JSON checkpoint using `schemas/continuity-checkpoint.schema.json` and the example at `examples/continuity-checkpoint.example.json`. Include stage status, artifact names/hashes when known, source availability, fallback details, open items, and one next action.
8. **Resume later without duplication.** When the failed service returns, use the checkpoint and idempotency keys to resume only pending stages. Preserve previously approved outputs unless their inputs changed.

## Component fallback matrix

| Failed component | Manual ChatGPT fallback | What must be disclosed |
|---|---|---|
| Cloudflare Worker/API | Continue the request directly in ChatGPT; prepare the same structured outputs | Hosted API unavailable; no server job was submitted |
| R2 storage | Use the source already attached in chat; preserve internal local artifacts and checkpoints when supported | Cloud persistence and cross-device availability are unavailable |
| Queue or Workflow | Execute stages sequentially in the current conversation and keep a stage ledger | No background execution, automatic retry, or progress after the session ends |
| AI Gateway / Workers AI | Use the current ChatGPT model and available vision/reasoning; use a secondary provider only when already authorized and available | Provider/model and any quality or cost differences |
| Supabase / PostgreSQL / pgvector | Keep structured state in JSON checkpoint and project files; defer indexing/sync | Persistent database, graph traversal, and semantic retrieval unavailable |
| Cloudinary | Work from original files already in chat; use available image/file tools for manual crops, notes, and variants | Automated transformations, media search, or Cloudinary analysis not executed |
| OCR / segmentation / detection | Read visible text manually; create human-reviewed boxes and layer descriptions; label uncertain regions | No engine confidence or pixel-accurate masks are available |
| Renderer / browser | Continue internal HTML/SVG/CSS work, but withhold customer delivery until a real render and required verification are available | No render means delivery is blocked; never provide an unverified HTML candidate |
| Visual QA / metric engine | Use genuine available image comparison and visual inspection; if required metric verification is unavailable, withhold final delivery | Do not invent SSIM, LPIPS, IoU, ΔE, Pixelmatch, MAE, or mismatch values |
| Figma | Preserve an internal SVG/HTML/token mapping for a later authorized Figma operation | No Figma nodes or editable Design layers were created; no mapping bundle is customer-delivered in reconstruction handoff |
| Source/version history service | Preserve an internal local source export and change note; sync when the service returns | Remote history or backup was not updated |
| Plugin invocation | Continue with the same instructions in the current ChatGPT conversation | Plugin routing is unavailable; host capabilities still govern execution |
| Any integration together | Fall back to the current ChatGPT conversation and available host tools; produce the best complete result possible | List each missing automated capability and any resulting verification gap |

## Metering and reminder behavior

Deliver the answer first. Usage metering is best-effort and reconciled after delivery. The current Pickko baseline is 100 free completed cycles. Crossing that allowance must not cut off an in-progress request. A friendly reminder is appended only after the answer, at most once every 20 minutes, and skipped whenever reminder state is unavailable or uncertain. Never wait for a metering or reminder write before returning the deliverable.

If a provider has genuinely exhausted its available capacity, use another already-authorized route or continue with the current ChatGPT model. Disclose any quality or verification difference. This is not a promise of unlimited external compute or funding.

## Manual completion standard

Preserve all of the following internally: reference analysis and unknowns, layer manifest, production methods, asset provenance, source files, renders, comparison evidence, defect corrections and continuity checkpoint. Do not expose them as a substitute for the final output.

For reconstruction jobs, the only customer-facing deliverable is one `DELIVERABLE_VERIFIED` standalone HTML file. If rendering, comparison or any required gate is unavailable, do not provide a partial source file or candidate HTML. State the exact blocker concisely. If the source image is unavailable, ask only for that exact missing input.

## Checkpoint and privacy rules

- Never put API keys, passwords, auth headers, access tokens, signed URLs, or secrets into a checkpoint.
- Do not embed customer files or image bytes in checkpoint JSON. Record safe names, hashes, and availability instead.
- Mark private customer content accurately. Do not call a checkpoint safe to share if it contains sensitive project facts.
- For a new ChatGPT conversation, tell the user to attach the original reference files plus the checkpoint if the attachments are not carried over.
- A checkpoint is recovery metadata, not a backup of the original binary assets.

## Limits of the fallback

ChatGPT manual mode is available only while ChatGPT and the required host capabilities remain accessible. If ChatGPT itself is unavailable, preserve an internal checkpoint and local project state for later resumption. Do not turn those recovery files into reconstruction deliverables. Never promise autonomous work after the host session ends.

## User-facing status pattern

Use a short, useful message:

> The automated media service is unavailable. I’m continuing the reconstruction internally using the original reference and approved layer plan. Final HTML delivery remains blocked until rendering and required metric-based verification are complete.

Avoid blaming the user, exposing raw infrastructure errors, or stopping at “try again later.”

## Completion report

Report four things: what continued manually, what was actually completed, what remains limited or unverified, and the checkpoint/next action. Preserve all successful outputs from before the outage.

See [the continuity quick reference](references/CONTINUITY-QUICK-REFERENCE.md) for the component map, checkpoint fields, and acceptance gates.


## Final HTML-only delivery remains mandatory

Fallback changes the execution route, not the customer deliverable. Continue manually using accessible source files and host tools, but keep manifests, asset crops, source code, previews, reports, checkpoints and any handoff briefs internal. Do not send a partial HTML candidate if rendering or required QA is unavailable. Deliver only one standalone HTML file after `DELIVERABLE_VERIFIED`; otherwise state the missing verification and preserve the same job for continuation.
