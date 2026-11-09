# Persistent design memory architecture

## Ownership map

| Data | System of record | Notes |
|---|---|---|
| Project/layer/asset/evidence/QA metadata | Supabase PostgreSQL | Canonical structured metadata |
| Graph nodes and edges | PostgreSQL tables | Do not add a separate graph DB before measurement |
| Vector index | pgvector | Single primary vector index for MVP |
| Binary assets | Cloudflare R2 | Immutable originals plus separately-versioned derivatives |
| Source/code/skills/migrations | GitHub | Versioned implementation and governance |
| Human knowledge views | Notion | Non-authoritative summaries linked to canonical records |

## Suggested tables

`projects`, `designs`, `layers`, `assets`, `asset_versions`, `prompts`, `design_patterns`, `recipes`, `design_tokens`, `graph_nodes`, `graph_edges`, `embeddings`, `qa_runs`, `defects`, `corrections`, `evidence`, `learning_events`.

## Graph node types

`PROJECT`, `REFERENCE`, `DESIGN`, `LAYER`, `ASSET`, `IMAGE`, `FONT`, `COLOUR_PALETTE`, `TYPOGRAPHY_SYSTEM`, `LAYOUT_PATTERN`, `DESIGN_TOKEN`, `PROMPT`, `GENERATION`, `RECONSTRUCTION_RECIPE`, `COMPONENT`, `QA_RESULT`, `DEFECT`, `CORRECTION`, `LICENSE`, `EVIDENCE`.

## Relationships

`CONTAINS`, `DERIVED_FROM`, `USES`, `GENERATED_BY`, `USES_PATTERN`, `USES_TOKENS`, `PARENT_OF`, `PRODUCED`, `IDENTIFIES`, `FIXES`, `REUSES`, `HAS_LICENSE`, `SUPPORTED_BY`, `SUPERSEDES`.

## Trust lifecycle

`NEW` -> `TESTED` -> `VERIFIED` -> `CANONICAL`. Transitions require evidence and policy. Only a human-approved operation may promote to `CANONICAL`.

## Retrieval features

Combine vector similarity, graph traversal, structured filters, current project context, source reliability, QA evidence, licensing and version status. A previous score proposal used V/G/C/Q/L/P weights of 0.30/0.20/0.20/0.15/0.10/0.05. Those are hypotheses; benchmark on held-out retrieval cases. Licence incompatibility and hard quality failure are exclusion gates.

## Cloudflare stages

R2 is the binary storage layer. Workers may provide API endpoints. Queues buffer independent background jobs. Workflows coordinate multi-step durable jobs. Durable Objects are reserved for stateful coordination needs. D1 is not selected. Vectorize is not selected as a primary vector store. Add services only when a measured requirement exists.
