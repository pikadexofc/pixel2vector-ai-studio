---
name: design-memory-curation
description: Use when turning completed design projects into reusable, provenance-aware assets, patterns, recipes, tokens, QA lessons, and structured design knowledge.
---

# Design Memory Curation
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

A completed project produces two internal outcomes: the finished design and reusable evidence-backed knowledge. The only customer-facing reconstruction deliverable is one verified standalone HTML file; the knowledge record remains internal. Store machine state once and expose it through controlled retrieval, rather than creating competing sources of truth.

## Selected ownership architecture

- Supabase PostgreSQL: structured project, design, layer, asset, evidence, graph, QA, and learning metadata.
- PostgreSQL graph tables: nodes and typed edges; a separate graph database is deferred until workload benchmarks justify it.
- pgvector: initial primary semantic index. Do not add Cloudflare Vectorize as a competing primary vector store without a measured reason.
- Cloudflare R2: binary originals, generated assets, masks, renders, and immutable artefact versions.
- GitHub: versioned source, schemas, migrations, scripts, skills, tests, and decisions.
- Notion: human-readable knowledge interface and generated documentation, not the machine system of record.
- Cloudflare Workers, Queues, and Workflows: staged API and durable background orchestration once needed.

These services are selected architecture, not configured integrations. Never claim they exist or write to them unless the host provides an authorized connection and execution evidence.

## Learning workflow

1. Trigger only after a project completion event or explicit curation request.
2. Collect the exact source project, manifest, assets, prompts, compile report, render, QA report, defects, and corrections.
3. Extract metadata without mutating original artefacts.
4. Detect reusable assets, patterns, tokens, recipes, and failure cases. Record the source layer/project for each.
5. Deduplicate using cryptographic hash, perceptual hash, and metadata. Do not merge distinct source records solely because embeddings are similar.
6. Create embeddings only for approved text/image representations and record embedding model/version.
7. Create graph nodes and edges with provenance, timestamps, confidence, and evidence references.
8. Add all new records as `NEW`.
9. Promote to `TESTED` only after a defined evaluation; promote to `VERIFIED` only with repeatable evidence; promote to `CANONICAL` only with explicit human approval.
10. Publish human-facing summaries to Notion only as views or generated copies with links to canonical database records.

## Graph model

Node types include `PROJECT`, `REFERENCE`, `DESIGN`, `LAYER`, `ASSET`, `IMAGE`, `FONT`, `COLOUR_PALETTE`, `TYPOGRAPHY_SYSTEM`, `LAYOUT_PATTERN`, `DESIGN_TOKEN`, `PROMPT`, `GENERATION`, `RECONSTRUCTION_RECIPE`, `COMPONENT`, `QA_RESULT`, `DEFECT`, `CORRECTION`, `LICENSE`, and `EVIDENCE`.

Relationships include `CONTAINS`, `DERIVED_FROM`, `USES`, `GENERATED_BY`, `USES_PATTERN`, `USES_TOKENS`, `PARENT_OF`, `PRODUCED`, `IDENTIFIES`, `FIXES`, `REUSES`, `HAS_LICENSE`, `SUPPORTED_BY`, and `SUPERSEDES`.

## Retrieval

Combine vector similarity, graph traversal, structured filters, provenance reliability, QA quality, licence eligibility, and context compatibility. A previously discussed weighted score is a starting hypothesis only; tune it with retrieval benchmarks. Apply hard exclusion rules for incompatible licences, unusable resolution, untrusted provenance, or outdated assets.

## Output

Produce a learning-event record, proposed node/edge changes, provenance references, trust-state rationale, duplicate/conflict report, and any required approval. See [memory architecture](references/MEMORY-ARCHITECTURE.md).

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.


## Reconstruction baseline retained in v1.0.0 (first integrated in v0.3.0)

Use `knowledge/reconstruction-baseline-v1.0/` as the evidence-backed baseline from the Legal Systems cover workflow, SubPilot poster and After the Noise banner. Treat the evidence classes and limitations in that archive as authoritative. In particular, keep source-recorded claims distinct from independently verified artifacts, preserve unresolved defects, and do not promote hypotheses to canonical rules without validation.

Learning artifacts, manifests, render images, QA records, and asset registers remain internal. The reconstruction customer receives only the final verified standalone HTML file.
