# PixelPerfect Studio module roadmap

| Module | Name | Main responsibility | Dependencies |
|---|---|---|---|
| M00 | Foundation | repo, instructions, CI, governance, toolchain | none |
| M01 | Contracts | canonical schemas and cross-runtime types | M00 |
| M02 | Ingestion | upload, metadata, hashes, orientation normalization | M01 |
| M03 | Forensics | region, OCR, geometry, color, gradient, masks | M01/M02 |
| M04 | Asset intelligence | source search, licence, deduplication, asset registry | M01/M02 |
| M05 | Reconstruction | deterministic manifest compiler and offline HTML/SVG | M01/M03/M04 |
| M06 | Visual QA | fixed renders, differences, region scores, defect reports | M01/M05 |
| M07 | Memory foundation | Supabase schema, graph/evidence records, RLS | M01 |
| M08 | Retrieval | pgvector plus graph traversal and evaluation | M07 |
| M09 | Cloudflare runtime | private R2, Workers, Queues and Workflows | M01/M02 |
| M10 | Learning curator | event ingestion, knowledge candidates, promotion gates | M03/M04/M06/M07/M08/M09 |
| M11 | Orchestrator | roles, states, approvals, retries, budgets | M01/M03-M10 |
| M12 | Skill library | tested reusable skills and evaluations | M00-M11 |
| M13 | Figma bridge | token/layer mapping and import/export checks | M01/M05/M06 |
| M14 | Operations | security, observability, backup, release and recovery | M00-M13 |

Each module receives its own specification, implementation plan, test plan, runbook, and acceptance report. Avoid placeholder production code. Implement incrementally after its plan is approved.
