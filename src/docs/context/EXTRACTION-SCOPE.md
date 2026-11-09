# Conversation knowledge extraction scope

**Extraction date:** 2026-11-03  
**Product:** PixelPerfect Studio  
**Rule:** Preserve operational design and engineering knowledge. Do not export the raw personal conversation as a dataset.

## Sources reviewed

1. Current conversation instructions defining the high-fidelity reconstruction and persistent learning objective.
2. The earlier PixelPerfect Studio master architecture and M00 foundation specification supplied in the working directory.
3. Historical conversation memory describing the visual forensics pipeline, asset methods, layer manifest, deterministic render and QA loop, and memory architecture.
4. Historical design-system and creative preferences relevant to design and brand outputs.
5. GitHub repository metadata and README-level evidence for `pikadexofc/pixelpie-creator-index`, `pikadexofc/aesthetic-iq`, `pikadexofc/cleaning-image-production-workflow`, and `pikadexofc/revforge-tools`.
6. Current official OpenAI Plugin and Agent Skills documentation checked on 2026-11-03.
7. The installed Plugin Autopilot and Plugin Creator Plus workflow guidance.

## Evidence strength

| Source | Evidence captured | Boundary |
|---|---|---|
| Master architecture | Full text copied into `docs/architecture/MASTER-DESIGN.md` | Existing selected architecture, not implemented infrastructure |
| M00 specification | Full text copied into `docs/architecture/M00-FOUNDATION.md` | Proposed module plan, not completed implementation |
| Conversation summaries | Operational rules rewritten into Skills and references | Summary-backed context, not verbatim transcript extraction |
| GitHub README files | Repository purpose and stated capabilities | README claims only; no source-code audit or runtime test |
| OpenAI developer documentation | Manifest and Skills package format, local marketplace model | Current documentation may change; verify before submission |
| Autopilot / Creator Plus skills | Workflow contracts and validation expectations | These are installed workflow instructions, not OpenAI product endorsements |

## Preserved operational knowledge

- Visual reference forensics and confidence/evidence discipline.
- Exact coordinate convention, EXIF normalization, palette and gradient analysis, OCR boundaries, segmentation and asset detection.
- Per-layer production selection: `GENERATE`, `SOURCE`, `CODE`, `SVG`, `TYPOGRAPHY`.
- Layer-manifest structure and deterministic compilation.
- Exact-size fixed-artboard HTML/CSS/SVG delivery and offline packaging.
- Three-stage QA: structural, fidelity, and finishing, with pixel and region measurements.
- Provenance, licence compatibility, immutable originals, variants, and hashes.
- Persistent knowledge design using Supabase/PostgreSQL graph tables/pgvector, Cloudflare R2, GitHub and Notion.
- Learning trust lifecycle: NEW, TESTED, VERIFIED, CANONICAL.
- Hybrid retrieval using vectors, graph traversal, structured filters, evidence, licensing and quality.
- Agent orchestration, state transitions, approvals, retries, budgets, logs, and fail-closed rules.
- Relevant style preferences and the conditional Editorial Neo-Brutalist Collage modes.

## Deliberate exclusions

The plugin does not contain sensitive personal context, health or substance-use details, personal finances, relationship histories, precise location, private contact details, passwords, tokens, API keys, client-confidential content, or raw private conversation logs. It also does not redistribute private source code from unrelated plugins or third-party assets. These items are irrelevant to the plugin's user job and would create unnecessary privacy and publication risk.

## Conflicts and precedence

The newest confirmed architecture selection overrides older alternatives. Historical preferences remain only when relevant and not superseded. See `DECISION-REGISTER.md` for specific precedence decisions.
