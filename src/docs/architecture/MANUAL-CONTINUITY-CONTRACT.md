# Manual Continuity and Graceful Degradation Contract

**Status:** Required product behavior, approved by product owner on 2026-11-03  
**Applies to:** ChatGPT Plugin, web application, reconstruction engine, storage, media services, AI providers, database, workflow runner, QA, Figma bridge, and delivery.

## Product promise

User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task. A temporary integration failure must not force a customer to abandon a design job or restart from zero. When the current ChatGPT conversation remains available, PixelPerfect Studio must switch to a manual ChatGPT workflow and continue every task that the available host can complete. The product must preserve completed work, identify limitations, and provide a resumable checkpoint.

This is a continuity promise, not a promise that unavailable tools can somehow be executed. A manual workflow may preserve the ability to continue the job while losing automation, speed, numerical verification, background execution, or cloud persistence. Those differences must be explicit. For reconstruction jobs, manual mode does not waive the final standalone HTML verification gate.

## Three operating modes

| Mode | Trigger | Behavior | User-facing status |
|---|---|---|---|
| `AUTOMATED` | Required services and host tools are available | Execute the complete pipeline with normal automated QA | Automated processing |
| `MANUAL_CHATGPT` | One or more integrations fail, but ChatGPT and relevant host capabilities remain available | Continue sequentially in the current conversation; reuse available files and create a checkpoint | Continuing manually in ChatGPT |
| `LOCAL_RECOVERY` | ChatGPT is unavailable or cannot access required tools | Preserve internal local project files and private checkpoint; no cloud dependency is required to retain progress | Recovery state retained internally |

The state machine must make transitions visible and reversible. A fallback mode must never silently downgrade a verification claim.

## Global fallback rules

0. Deliver the answer first. Run usage, entitlement, reminder, and analytics reconciliation afterward and off the customer-facing critical path. A failed usage write is recorded as pending; it does not reject or interrupt the task. A reminder is shown only after delivery and at most once every 20 minutes.

1. Preserve user intent, source assets, approved decisions, and completed artifacts.
2. Reuse current-conversation attachments when they remain accessible; ask for re-upload only when an attachment is genuinely unavailable.
3. Switch once after a bounded transient retry. Permission, authentication, quota, policy, invalid-input, and budget failures require correction or fallback, not retry loops.
4. Continue with the narrowest available ChatGPT host capability: visual inspection, file reading, Python, code authoring, rendering, or artifact creation.
5. Execute pipeline stages sequentially in fallback mode. Do not imply that queues, Workflows, scheduled jobs, or background execution still operate.
6. Preserve the same output contract in every execution mode. For reconstruction jobs, only one final verified standalone HTML file may be delivered. If rendering or required QA cannot be completed, deliver no file and state the blocker.
7. Label each internal artifact as manually produced, automatically produced, or pending. Record tool availability and evidence. Keep all manifests, crops, masks, assets, fonts, source files, previews, diffs, reports and checkpoints internal.
8. Never fabricate OCR confidence, segmentation masks, metric scores, execution logs, hashes, renders, uploads, storage writes, or Figma changes.
9. Keep a checkpoint before ending or changing mode. The checkpoint excludes credentials and binary file contents.
10. When services return, resume only pending or invalidated stages. Use input hashes and idempotency keys to prevent duplicate work.

## Service-by-service fallback ownership

| Component | Normal responsibility | Fallback owner | Manual substitute | Deferred capability |
|---|---|---|---|---|
| Plugin invocation | Route to specialist Skills | Current ChatGPT conversation | Invoke the relevant Skill instructions directly in context | Plugin-specific invocation telemetry |
| Orchestrator | Sequence stages and status | ChatGPT model | Sequential stage ledger and checkpoint | Background dispatch and automatic orchestration |
| Visual model/inference | Describe, reason, detect visual details | ChatGPT vision/reasoning when available | Manual region inspection and uncertainty ledger | Provider-specific inference metrics |
| OCR | Extract copy and text boxes | ChatGPT vision and user review | Transcribe visible copy; record approximate boxes and uncertainty | OCR confidence and exact text-line geometry |
| Segmentation/detection | Produce object masks and detections | Human-guided analysis in ChatGPT | Hand-authored rectangles, polygons, or descriptive regions | Machine masks, detector confidence and automatic contours |
| Cloudinary | Transform, analyze, search and deliver media | ChatGPT plus available file/image tools | Use original attached asset and specify manual crop/variant steps | Cloudinary transformation IDs, automated visual search and delivery URLs |
| R2 | Store originals, intermediates and exports | Internal local project storage | Preserve source and intermediate files locally; never expose reconstruction work products as separate handoff files | Shared persistence and remote object delivery |
| Workers/API | Accept customer jobs and expose product APIs | Current ChatGPT conversation | Perform the request directly in the conversation | Hosted API calls and customer web-app execution |
| Queues/Workflows | Durable background processing | ChatGPT stage ledger | Execute steps sequentially and preserve progress | Background execution, durable retries and long-running work after session closure |
| Supabase | Structured records, graph, permissions and vector metadata | JSON checkpoint and project export | Maintain structured JSON files and defer sync | Shared database writes, graph traversal and server-side retrieval |
| Vector search | Semantic retrieval | Current conversation and available file search | Search the available project references manually | Embedding-based ranking and recall |
| AI Gateway / Workers AI | Route inference, cache and control spend | ChatGPT model or an already-authorized available provider | Manual model invocation through the host | Gateway logs, provider fallback policy and gateway budgets |
| Compiler/renderer | Build exact-size HTML/SVG and render | ChatGPT code/file tools | Author editable source; render only with an available runtime | Reproducible hosted build if no execution runtime is available |
| Visual QA | Compare pixels, structure, semantics and regions | ChatGPT vision plus available local execution | Human visual review, defect ledger and correction plan | Numerical metric scores if no metric runner is available |
| Figma bridge | Create/import editable design structures | Internal SVG/HTML/token mapping | Prepare recovery inputs internally for a later authorized Figma operation | Live Figma node writes/imports |
| Learning curator | Persist verified patterns and provenance | Checkpoint and project knowledge files | Record candidates with evidence and pending sync status | Persistent cross-project memory until database returns |
| Source/version history | Track changes and releases | Local copy and release note | Save local source snapshot and change summary | Remote backup, review and release history |
| Delivery service | Provide the approved final artifact | ChatGPT file/artifact capability | Deliver exactly one HTML file only after `DELIVERABLE_VERIFIED`; otherwise state blocker with no file | Hosted download links and cross-device retrieval |

## Customer interaction requirements

The customer must see:

- one clear notice that automatic processing is degraded;
- confirmation that the job is continuing in ChatGPT when possible;
- no request to repeat information already retained;
- a concise distinction between verified completion and the exact blocker;
- the next useful action, not an infrastructure error dump.

For reconstruction jobs, checkpoint data remains internal. Do not expose it as a separate file or bundle. If the session must be resumed elsewhere, preserve the checkpoint in the product's internal state or continue from the retained conversation context.

The fallback should not require the customer to understand Cloudflare, Cloudinary, Supabase, queues, providers, or internal service boundaries.

## Continuity checkpoint

An internal checkpoint records project identity, canvas, current stage, completion state, source input availability, stage ledger, internal artifact references, failure/fallback details, limitations, open items, and next action. Use the schema at `schemas/continuity-checkpoint.schema.json`.

The checkpoint does not embed binaries or secrets. Keep source binaries in the existing project attachment/storage context. For reconstruction jobs, do not ask the customer to download or attach a checkpoint as a deliverable. Reuse retained conversation context and accessible files wherever possible.

## Acceptance tests

0. Metering outage before or during a request: the result is still delivered; the usage event is marked pending for safe reconciliation.
0a. Quota threshold reached during a request: the current task completes; reminder eligibility is checked only after delivery.
0b. Reminder state unavailable: skip the reminder and deliver the result without delay.

The product is not continuity-ready until these scenarios pass:

1. Cloudinary timeout after upload: original image remains usable and the task continues manually.
2. Cloudflare API outage before processing: ChatGPT performs the available analysis and exports a checkpoint.
3. R2 unavailable after reference upload: no source loss; local/chat output route remains usable.
4. Supabase outage mid-project: approved manifest and stage ledger survive in checkpoint; no duplicate decisions are created on resume.
5. Workflow/Queue failure: sequential manual continuation completes available stages; no false background progress is reported.
6. AI provider failure: switch to current ChatGPT capability or stop only the unsupported subtask with an explicit limitation.
7. Renderer unavailable: keep HTML/SVG source internal; final delivery is blocked until a genuine render and required verification exist.
8. Visual metric service unavailable: qualitative review is separated from numerical QA; no synthetic scores appear.
9. Figma unavailable during reconstruction: preserve internal SVG/HTML/tokens/mapping for recovery; do not attach them as reconstruction deliverables, and do not claim a Figma write.
10. ChatGPT host unavailable: retain an internal/local checkpoint and project files for resumability where the host environment permits; do not present these as reconstruction deliverables, and make no promise of an unavailable ChatGPT fallback.
11. New conversation resume: checkpoint plus required source files restore stage state without asking for known requirements again.
12. Secret scan: checkpoint contains no credentials, tokens, signed URLs, or secret values.

## Release gate

A release must include the manual fallback Skill, this contract, schema and valid example, orchestrator integration, registry entry, plugin capability description, and passing tests. Service-level automated failover, offline local persistence, and browser UI controls remain implementation work and must not be advertised as already deployed.


## Reconstruction-specific customer output

The reconstruction customer receives exactly one `DELIVERABLE_VERIFIED` standalone HTML file. All build and verification evidence remains internal. A service outage, unavailable renderer, missing browser capture, missing calibrated comparison profile or failed acceptance gate blocks file delivery; it never authorizes a partial HTML, source bundle, preview or ZIP handoff. See `resources/FINAL-HTML-ONLY-DELIVERY.md`.
