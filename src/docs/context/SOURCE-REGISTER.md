# Source register

| Source | Inspection method | Disposition | Confidence / limitation |
|---|---|---|---|
| `/mnt/data/pixelperfect-studio-blueprint/docs/architecture/MASTER-DESIGN.md` | Read full local document and copied into this package | `preserve_reference` | High for the recorded decisions; document itself is a proposal, not implementation evidence |
| `/mnt/data/pixelperfect-studio-blueprint/docs/modules/M00-FOUNDATION.md` | Read full local document and copied into this package | `preserve_reference` | High for module requirements; not evidence that M00 has been implemented |
| `pikadexofc/pixelpie-creator-index` | Read repository metadata and README | `reference_only` | Public provenance index; not source of private plugin implementation |
| `pikadexofc/aesthetic-iq` | Read repository metadata and README | `reference_only` | README describes a browser-side image analysis tool; no code audit performed |
| `pikadexofc/cleaning-image-production-workflow` | Read repository metadata and README | `reference_only` | README describes evidence-bound image review; no source/test execution performed |
| `pikadexofc/revforge-tools` | Read repository metadata and README | `internal_reference_only` | Private repo; README-level only. No private files copied |
| Conversation memory and summaries | Extracted stable operational facts and decisions | `compile_skill` / `reference_only` | Summarized context, not raw transcripts |
| OpenAI Plugin architecture docs | Current official docs retrieved on 2026-11-03 | `reference_only` | Official contract as observed on retrieval date |
| Agent Skills specification | Current official specification retrieved on 2026-11-03 | `reference_only` | Agent Skills standard may evolve |
| Plugin Autopilot | Installed skill instructions read | `workflow_reference` | Workflow guidance, not itself proof of official OpenAI approval |
| Plugin Creator Plus | Installed skill instructions read | `workflow_reference` | Packaging helper is skills-only and has older assumptions; adapted checks are documented |
| User-supplied plugin icon | Inspected `pickko_plugin_icon_pack.zip`, including SVG master, 12 PNG sizes, favicon, and manifest; imported unchanged under `assets/icon-pack/` | `preserve_asset` | File-level dimensions and manifest paths checked for 0.2.1; no OpenAI publisher approval implied |

