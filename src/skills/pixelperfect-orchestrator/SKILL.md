---
name: pixelperfect-orchestrator
description: Use when converting an uploaded image into a high-fidelity fixed-size HTML design with independently addressable layers and separate visual assets.
---

# PixelPerfect Orchestrator

## Product boundary

The primary product is **image to editable layered HTML design**. The HTML is a fixed-size design artboard, not a responsive website. Reconstruct every meaningful visual component as its own independently addressable HTML/CSS, SVG or embedded image layer. Use separate extracted or generated PNG assets when raster imagery is the best method. Prioritize visual fidelity and component quality over web performance optimization, SEO, mobile reflow or application features. The only customer-facing reconstruction deliverable is one final verified standalone HTML file. See `docs/product/PRODUCT-DEFINITION.md`.
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Coordinate specialist work as a controlled state machine. Inference may propose; deterministic stages consume approved, versioned inputs. The orchestrator owns sequencing, status, approvals, retries, evidence, and final reporting. The user-facing task outcome outranks usage metering, entitlement bookkeeping, reminders, analytics, and infrastructure health.

## Pipeline states

Use these states in order, with explicit transition evidence:

1. `INTAKE`: confirm user goal, source reference, canvas, deliverable, constraints.
2. `FORENSICS`: normalize reference and produce structured observations with confidence.
3. `LAYER_PLAN`: create and review the complete layer manifest before asset production.
4. `ASSET_PLAN`: choose `SOURCE`, `GENERATE`, `CODE`, `SVG` or `TYPOGRAPHY` per meaningful layer. Source-extract reference-specific details first; use separate PNG generation when source extraction cannot meet quality.
5. `ASSET_READY`: inspect every extracted or generated asset separately at intended output size; verify crop, perspective, mask edges, lighting, resolution and provenance, then freeze selected versions.
6. `COMPILE`: compile the frozen manifest and assets into a deterministic composition.
7. `RENDER`: render at exact target dimensions with recorded environment.
8. `QA`: run structural, fidelity, and finishing checks; record defects and metrics.
9. `CORRECT`: repair only defective layers or regions, then rerender and re-evaluate.
10. `LEARN`: extract reusable patterns, assets, recipes, failures, and corrections with evidence.
11. `DELIVER`: release exactly one final verified standalone HTML file; preserve all other build evidence internally.

A transition is valid only when the previous stage's required outputs exist and pass its gate. A missing artifact never becomes an assumed success. Keep the layer manifest, source assets, generated PNGs, previews and QA evidence internal. Never hand these to the customer as reconstruction deliverables.

## Specialist routing

- `setup`: intake and readiness.
- `visual-reference-forensics`: reference measurements and confidence.
- `asset-intelligence`: asset strategy, source research, generation review, provenance.
- `deterministic-reconstruction`: frozen manifest compilation.
- `visual-quality-assurance`: render inspection and regression.
- `design-memory-curation`: evidence-backed learning and retrieval design.
- `design-system-architecture`: design tokens, style decisions, and preferences.
- `workspace-engineering`: repository/file operations and technical verification.
- `manual-fallback-continuity`: continue the same customer job in ChatGPT when an integration, model, renderer, storage service, or host tool fails.

## Control rules

- Build a dependency graph before dispatching parallel work. Parallelize only independent stages with immutable inputs.
- Freeze the layer manifest before final asset production; any structural change increments its version and invalidates affected downstream work.
- Give each job, artifact, asset, render, QA run, and learning event a stable identifier.
- Record `input_hashes`, `tool_versions`, `attempt`, `started_at`, `completed_at`, `status`, and evidence references.
- Retry only transient failures, with bounded attempts and exponential backoff plus jitter when an actual scheduler exists. Never retry destructive operations blindly.
- Do not let retries create duplicate assets or duplicate learning records. Use idempotency keys based on project, stage, input hashes, and operation version.
- Enforce human approval for ambiguous reference interpretations, licence uncertainty, material creative deviations, irreversible external changes, and promotion to `CANONICAL`.
- Track provider/model calls and resource consumption for internal planning only. Metering and telemetry are best-effort, non-blocking, and reconciled after delivery.
- If a tool or connection is absent, activate `manual-fallback-continuity`; continue in ChatGPT using a documented manual alternative whenever the host remains available. Mark only unsupported sub-capabilities as blocked and maintain a continuity checkpoint. Never block the current task because a usage, entitlement, analytics, or reminder write failed.

## Manual continuity is mandatory

Deliver the answer first. Usage metering is best-effort. A quota threshold must not interrupt an in-progress request; a reminder is eligible only after delivery and at most once every 20 minutes. See `resources/PRODUCT-EXPERIENCE-CONTRACT.md`.

Never leave the user at a dead end when a system or integration fails. If the current ChatGPT conversation remains available, activate `manual-fallback-continuity`, preserve all accessible inputs and completed outputs, and continue the remaining stages sequentially with available host tools. Do not ask the user to repeat known requirements or re-upload files that remain accessible in the current conversation.

Create or update a portable continuity checkpoint whenever a stage becomes blocked, the execution mode changes, or the session is about to end with unfinished work. The checkpoint records the current stage, completed work, source availability, artifacts, limitations, open items, and next action. It must never contain credentials, tokens, signed URLs, or binary file contents.

Manual fallback must preserve the deliverable intent but must not claim unavailable automation. If no renderer is available, keep the source internal and block customer file delivery. If no metric runner is available, preserve qualitative findings internally and block final delivery until the required numerical QA is available. If ChatGPT itself is unavailable, preserve an internal local checkpoint and project state for later resumption; do not expose those recovery files as reconstruction deliverables.

See `docs/architecture/MANUAL-CONTINUITY-CONTRACT.md` and `resources/MANUAL-FALLBACK-PROTOCOL.md` for the complete service matrix and acceptance tests.

## Completion gate

A reconstruction is `DELIVERABLE_VERIFIED` only when the frozen manifest, source/render dimensions, standalone runtime, all three QA passes, critical-region checks, defect closure and final HTML hash pass the acceptance contract. Apply calibrated numerical thresholds when a validated profile exists; otherwise the measured metrics remain diagnostic and a direct visual review bound to the exact reference/render hashes is mandatory. If required evidence is absent, delivery is blocked. Use `PIXEL_IDENTICAL` only after exact pixel equality is demonstrated.

## Output contract: one file only

Follow `resources/FINAL-HTML-ONLY-DELIVERY.md`. The only customer-facing deliverable is one final, verified, standalone `.html` file. Layer manifests, analysis, assets, source masks, fonts, previews, screenshots, difference maps, QA reports, stage ledgers, JSON files, READMEs and ZIP bundles are internal evidence, not customer deliverables.

Never expose a first-pass or unverified HTML candidate. If `DELIVERABLE_VERIFIED` cannot be reached, deliver no file; state the exact blocker in concise prose and preserve the work for continuation. Do not replace the final HTML with a preview or project bundle.

The internal stage ledger, manifest, asset register, render metadata and QA evidence must still be maintained for traceability. They remain internal by default.

See `resources/FINAL-HTML-ONLY-DELIVERY.md` and [pipeline contract](references/PIPELINE-CONTRACT.md).

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.
