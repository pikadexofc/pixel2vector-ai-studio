---
name: setup
description: Use when a user uploads an image or asks to convert a visual reference into a high-fidelity editable layered HTML design.
---

# Project Setup

## Product in plain language

PixelPerfect Studio turns a flat image into a structured, editable HTML design. It separates meaningful components into individual HTML/CSS, SVG and embedded PNG image layers, preserves the reference's fixed canvas dimensions, and delivers one verified standalone HTML file. This is a static design canvas, not a responsive website or app builder. Read `docs/product/PRODUCT-DEFINITION.md` for the canonical product scope.
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Prepare a bounded reconstruction job before analysis begins. This Skill is an intake and readiness workflow, not permission to provision cloud infrastructure. Do not require signup, payment details, quota checks, or account setup before helping with the task when the host can proceed without them.

## Required intake

Capture these fields when available:

- project name and purpose
- reference image or file, original source preserved
- native reference dimensions; default to the normalized original dimensions unless the user explicitly requests another canvas
- special must-preserve constraints; the default and only reconstruction deliverable is one verified standalone HTML file
- visual constraints and must-preserve elements
- allowed asset sources and licensing requirements
- deadline, effort, and compute constraints
- available host tools and connected services

Ask only for information that blocks the next action. Do not ask the user to describe visible facts, prepare a manifest, split the image into assets, find fonts, or specify routine implementation details. If the reference image is available, inspect it and proceed with sensible defaults.

## Readiness procedure

1. Inspect the attached reference and confirm its dimensions from file metadata when file tools exist.
2. Preserve the source file as immutable input. Create a normalized derivative only after recording its hash and orientation.
3. Resolve the requested canvas dimensions. If unspecified, use the reference's normalized pixel dimensions as the default and state that assumption.
4. For the default PixelPerfect workflow, treat an uploaded image as a faithful image-to-editable-layered-HTML reconstruction request. Do not silently convert it into a responsive website, app UI or new design concept. Only change the objective when the user explicitly asks.
5. Inventory available tools. Distinguish host-native image input, Python, shell, browser, image generation, Figma, and external service connectors. A skill cannot grant any of these tools.
6. Mark each external service as `connected`, `not connected`, or `not needed`. Never invent credentials or claim a cloud resource exists.
7. Produce an intake record and a readiness status: `ready`, `ready_with_assumptions`, or `blocked`.
8. Hand off to `pixelperfect-orchestrator` for stage planning.

## Stop conditions

Stop or ask one focused question when the target canvas, source ownership, required editability, or intended deliverable cannot be reasonably inferred. If a task requires Supabase, Cloudflare, Figma, or a provider account that is not connected, continue only with a local plan or explain the missing integration.

## Output contract

The intake brief and readiness record are internal. For reconstruction jobs, the only customer-facing deliverable is one final verified standalone HTML file. Do not attach or link manifests, previews, extracted assets, QA reports, source folders or ZIP bundles. If the required final verification cannot pass, do not send an HTML candidate; report the exact blocker concisely. Never claim that a workspace has been created, a service has been provisioned, or an asset has been processed unless the host produced evidence.

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.
