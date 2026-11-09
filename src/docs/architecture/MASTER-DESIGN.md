# PIXELPERFECT STUDIO
## Master Architecture and Delivery Blueprint

**Version:** 1.1.0  
**Status:** Architecture selected; module implementation plans require review  
**Date:** 2026-11-03  
**Owner:** PixelPie Media  

---

## 1. Mission

Build a reproducible visual reconstruction and persistent design-intelligence platform. Given a reference image and a production brief, the system must inspect the reference, identify and source or create the required assets, reconstruct the composition, render it at the exact target dimensions, measure defects, and preserve verified knowledge for future projects.

Every completed project produces two classes of output:

1. **Customer production output:** one verified standalone HTML file only. Layer manifests, source assets, rendered references, difference maps and QA reports are internal production evidence.
2. **Knowledge output:** reusable assets, patterns, tokens, recipes, decisions, defects, corrections, licences, provenance, and evaluation evidence.

The system must never confuse a plausible reconstruction with a verified reconstruction. Confidence, source provenance, visual differences, and unresolved defects remain inspectable.

## 2. Architecture decision

### Selected approach: modular monorepo with separated runtimes

Use one private repository for contracts, orchestration, services, scripts, tests, infrastructure definitions, documentation, and skills. Keep subsystem boundaries explicit so that a future service can be extracted without splitting the source of truth prematurely.

- **TypeScript / Node.js:** orchestration, CLI, API boundaries, schemas, workflow adapters, and browser automation.
- **Python:** computer vision, segmentation, image processing, OCR adapters, embeddings where appropriate, and quantitative evaluation.
- **PostgreSQL / Supabase:** structured metadata, evidence, relational graph, permissions, and vector retrieval through pgvector.
- **Cloudflare R2:** binary assets and immutable artefact versions.
- **Cloudflare Workers, Queues, and Workflows:** APIs and durable asynchronous execution when the relevant module is implemented.
- **GitHub:** source code, migrations, skills, schemas, CI, issue history, and versioned decisions.
- **Notion:** human-readable knowledge views and operating documentation, not a second system of record.

### Alternatives considered

| Approach | Benefit | Cost / risk | Decision |
|---|---|---|---|
| Modular monorepo | Shared contracts, atomic changes, one CI surface, easier early evolution | Requires strict package and service boundaries | **Selected** |
| Separate repository per service | Independent releases and permissions | Premature coordination overhead, duplicated schemas and CI | Reconsider only when ownership or deployment boundaries require it |
| Skill-first / prompt-only system | Fast initial experimentation | No deterministic compiler, durable evidence, or testable infrastructure | Not sufficient for the stated objective |

### Repository boundary

Create a new private repository named `pixelperfect-studio`. Do not repurpose `pixelpie-creator-index`; that repository remains a public evidence and provenance catalogue. Do not add client assets, private plugin source, credentials, or third-party material without rights review.

## 3. Runtime and toolchain baseline

These are proposed compatibility targets, not permission to install packages before the Module 00 plan is approved.

| Area | Starting target | Policy |
|---|---|---|
| Node.js | 26.x Active LTS | Pin exact patch in CI and runtime files; update through reviewed PRs |
| Package manager | pnpm 12.x | Pin exact release in `package.json` `packageManager` |
| Python | 3.14.x | Use `uv`; benchmark vision-library compatibility before freezing |
| TypeScript | Strict mode | No implicit `any`; generated types must derive from shared contracts |
| Contract format | JSON Schema Draft 2020-12 | Canonical machine-readable source for cross-runtime payloads |
| JS tests | Vitest | Unit and contract tests run in CI |
| Python tests | pytest | Unit and integration tests run in CI |
| Browser automation | Playwright | Deterministic viewport, browser version, and device scale factor |
| Image comparison | Pixelmatch plus independent mismatch-ratio calculation | Pixel threshold is not the same as whole-image mismatch percentage |

**Compatibility gate:** Python 3.14 is the conservative initial target for the computer-vision ecosystem. Python 3.15 may be evaluated, but must not become the production baseline until OpenCV, OCR, segmentation, and model dependencies pass the compatibility matrix.

## 4. Core system boundaries

### 4.1 Probabilistic intelligence plane

Handles tasks that require inference or discovery:
- visual interpretation and region detection
- OCR and typography candidate identification
- asset discovery and candidate ranking
- generation prompts and generated asset evaluation
- pattern discovery and semantic retrieval
- confidence estimation and ambiguity reporting

This plane proposes results. It does not silently override approved data or declare success without evidence.

### 4.2 Deterministic production plane

Handles tasks that must be repeatable:
- schema validation
- normalized coordinate calculations
- layer-manifest compilation
- asset packaging and hash verification
- HTML/CSS/SVG output
- fixed-viewport rendering
- image-difference calculations
- provenance and licence checks
- export packaging

Given the same validated manifest, asset hashes, compiler version, and render environment, this plane should produce equivalent output within documented rendering tolerances.

### 4.3 Evidence and control plane

Coordinates jobs, approvals, retries, immutable inputs, logs, costs, and final status. Every operation has a stable ID, parent job ID, input references, software version, attempt count, result status, and evidence references.

## 5. Planned modules and delivery order

| ID | Module | Primary outputs | Depends on |
|---|---|---|---|
| M00 | Repository foundation and engineering governance | Monorepo skeleton, agent instructions, CI, validation scripts, standards | None |
| M01 | Shared contracts and canonical data model | JSON Schemas, TypeScript/Python validation, event contracts | M00 |
| M02 | Reference ingestion and normalization | Upload pipeline, EXIF normalization, canonical image records, hashes | M01 |
| M03 | Visual forensics engine | Regions, OCR observations, palette samples, spatial gradients, geometry and masks | M01, M02 |
| M04 | Asset intelligence and provenance | Search adapters, deduplication, licence filters, asset registry metadata | M01, M02 |
| M05 | Deterministic reconstruction compiler | Layer manifest compiler, HTML/CSS/SVG renderer, offline package | M01, M03, M04 |
| M06 | Visual QA and regression engine | Playwright renders, diff maps, region scores, defect report | M01, M05 |
| M07 | Memory foundation | Supabase migrations, PostgreSQL tables, RLS, graph and evidence records | M01 |
| M08 | Hybrid retrieval | pgvector retrieval, graph traversal, metadata and licence filters, ranking evaluation | M07 |
| M09 | Cloudflare runtime integration | Private R2 adapter, Workers, Queue and Workflow adapters | M01, M02 |
| M10 | Learning curator | Project-completion ingestion, metadata extraction, validation and knowledge promotion | M03, M04, M06, M07, M08, M09 |
| M11 | Agent orchestrator | Agent roles, state machine, tool contracts, approvals, budgets and retries | M01, M03-M10 |
| M12 | Operational skill library | Tested reusable agent skills, skill registry, skill evaluation suite | M00-M11 as relevant |
| M13 | Figma interoperability | Token export, layer mapping, import/export validation | M01, M05, M06 |
| M14 | Operations and release hardening | Observability, backups, disaster recovery, security review, release process | M00-M13 |

Modules are delivered sequentially unless a dependency-free documentation or research task can be safely completed in parallel. No module is called complete until its acceptance criteria and verification commands pass.

## 6. Canonical knowledge model

### Node classes

`PROJECT`, `REFERENCE`, `DESIGN`, `LAYER`, `ASSET`, `IMAGE`, `FONT`, `COLOUR_PALETTE`, `TYPOGRAPHY_SYSTEM`, `LAYOUT_PATTERN`, `DESIGN_TOKEN`, `PROMPT`, `GENERATION`, `RECONSTRUCTION_RECIPE`, `COMPONENT`, `QA_RESULT`, `DEFECT`, `CORRECTION`, `LICENSE`, `EVIDENCE`.

### Relationship classes

`CONTAINS`, `DERIVED_FROM`, `USES`, `GENERATED_BY`, `USES_PATTERN`, `USES_TOKENS`, `PARENT_OF`, `PRODUCED`, `IDENTIFIES`, `FIXES`, `REUSES`, `HAS_LICENSE`, `SUPPORTED_BY`, `SUPERSEDES`.

Every edge that affects retrieval or a decision should preserve provenance, timestamp, source record, and confidence where applicable.

### Trust lifecycle

- `NEW`: captured but not independently validated.
- `TESTED`: exercised in a defined workflow or test.
- `VERIFIED`: backed by repeatable execution or inspectable evidence.
- `CANONICAL`: explicitly approved stable standard.

Agents may propose records and relationships. They may not promote evidence to `CANONICAL` without an explicit approval policy.

## 7. Data ownership and system of record

| Data | System of record | Rule |
|---|---|---|
| Project, layer, asset, prompt and QA metadata | Supabase PostgreSQL | Structured metadata and relations only |
| Vector embeddings | pgvector in Supabase initially | Keep a single primary vector index until benchmarks justify a second |
| Original and processed binary assets | Cloudflare R2 | Immutable originals; processed variants reference their parent |
| Source code, schemas, migrations, tests, skills | GitHub | Versioned and reviewable |
| Human-facing knowledge pages | Notion | Generated or linked from canonical records; not authoritative for machine state |
| Local caches and temporary renders | Local worker storage | Rebuildable; never the only copy of an approved artefact |

Do not introduce a separate graph database or Cloudflare Vectorize as a second primary index in the MVP. Benchmark pgvector plus relational graph traversal first.

## 8. Asset integrity and licensing

Every asset record must include, where applicable:
- stable asset ID and immutable original object key
- dimensions, format, colour profile, alpha/transparency state
- cryptographic content hash and perceptual hash
- semantic tags and machine-generated descriptions
- source URL or generation record and prompt
- source project and layer reference
- licence, attribution requirements, usage restrictions, and review status
- processing history and parent/variant relationships
- validation state and evidence references

Similarity is not suitability. Reject candidates with incompatible rights, insufficient resolution, unsupported transparency, wrong subject, or incompatible crop requirements. Preserve source and licence evidence.

## 9. Global engineering rules

1. No production code without a failing test first, except agreed generated code and pure configuration.
2. Validate inputs at every trust boundary.
3. Prefer explicit interfaces, small modules, and dependency injection.
4. Keep original inputs immutable; create versioned derivatives.
5. Never store secrets in source, fixtures, logs, prompts, or public artefacts.
6. Use least-privilege credentials and private object storage by default.
7. Require provenance for external and generated assets.
8. Never infer exact font identity, image licence, or pixel-perfect status without evidence.
9. Every asynchronous job must be idempotent, resumable, bounded by retry policy, and observable.
10. All timestamps use UTC in storage; user-facing timezones are presentation-only.
11. Every module has a defined owner, inputs, outputs, failure modes, tests, runbook, and acceptance gate.
12. Record unresolved uncertainty rather than silently replacing it with assumptions.

## 10. Module 00 scope

### Included
- repository and directory conventions
- root agent instructions and contributor workflow
- runtime and package-manager pinning
- common scripts for environment diagnostics, repository structure, links, and skill metadata
- CI workflow and security baseline
- documentation templates, ADR format, module specification template
- skill registry and skill-authoring governance

### Excluded
- Supabase project or migration changes
- Cloudflare account, bucket, Worker, Queue, or Workflow creation
- AI provider credentials or model calls
- computer-vision dependencies and inference
- production UI or reconstruction algorithms
- Figma API integration

## 11. Module 00 acceptance criteria

1. A clean checkout can install from lockfiles without mutating them.
2. The repository doctor reports required and optional dependencies distinctly and gives actionable remediation.
3. Repository validation fails on missing required paths or malformed configuration.
4. Skill validation fails on invalid names, missing `SKILL.md`, malformed frontmatter, missing triggers, or broken relative references.
5. Documentation link validation catches broken internal links while allowing explicitly external links.
6. `pnpm verify` runs formatting, lint, type-check, unit tests, contract validation, documentation validation, and skill-structure checks.
7. GitHub Actions runs the same verification command on pull requests and protected branches.
8. No real credentials or provider resources are required to run the foundation test suite.
9. All secrets are represented only by documented variable names in `.env.example`.
10. All new skills remain `draft` until their behavioral evaluation is completed.

## 12. Explicit non-goals

- Automatically learning unverified information as canonical truth.
- Claiming that a generated image is an exact reconstruction without quantitative comparison.
- Replacing Figma with a non-editable HTML screenshot.
- Treating a vector embedding as a licence or provenance record.
- Creating multiple primary sources of truth for the same metadata.
- Adding infrastructure products merely because they are available.

## 13. Key risks and mitigations

| Risk | Mitigation |
|---|---|
| Vision dependencies lag Python releases | Maintain a compatibility matrix and pin the last fully supported runtime |
| Schema drift across TypeScript and Python | JSON Schema is canonical; generate or validate both runtime models from it |
| Duplicate assets inflate storage and retrieval noise | Combine content hash, perceptual hash, variant lineage, and licence-aware grouping |
| Agent-generated facts become canonical without evidence | Trust lifecycle, evidence references, and explicit promotion approval |
| Cloud workflow retries duplicate side effects | Idempotency keys, transactional outbox/inbox patterns, and replay tests |
| Overbuilt architecture increases cost | Ship one useful vertical slice per module; add infrastructure only at its trigger point |

## 14. First end-to-end vertical slice

The first meaningful product slice after foundations is:

`reference.png → normalized reference record → analysis.json → layer-manifest.json → index.html → rendered.png → diff-report.json`

The first vertical slice can use local storage and deterministic fixture data. It must not depend on live AI credentials or cloud infrastructure. Cloud adapters are added after the local contracts and behavior are proven.

## 15. Approval boundary

This document records the selected overall architecture. Module 00 has its own implementation plan and acceptance criteria. No source code, dependencies, infrastructure, or remote repository state should change until the Module 00 plan is accepted and an execution workspace is agreed.

## 16. References

- Node.js release schedule: https://github.com/nodejs/Release
- Python active releases: https://www.python.org/getit/
- pnpm documentation and release information: https://pnpm.io/
- Supabase documentation: https://supabase.com/docs
- Cloudflare developer documentation: https://developers.cloudflare.com/
- JSON Schema: https://json-schema.org/draft/2020-12
- Playwright documentation: https://playwright.dev/docs/intro


## Mandatory Manual Continuity

Every integration and processing stage must have a ChatGPT manual fallback when the current conversation and relevant host capabilities remain available. See [Manual Continuity Contract](MANUAL-CONTINUITY-CONTRACT.md), the `manual-fallback-continuity` Skill, and the portable checkpoint schema. The automated service can be unavailable without making the customer's design job a dead end.
