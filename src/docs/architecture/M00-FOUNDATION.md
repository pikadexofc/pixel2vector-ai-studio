# M00 — Repository Foundation and Engineering Governance

**Status:** Proposed  
**Version:** 1.0.0  
**Parent:** `docs/architecture/MASTER-DESIGN.md`  

## 1. Outcome

A clean, private, reproducible monorepo that tells humans and agents how to work, validates its own structure, enforces baseline quality gates, and provides stable locations for all future modules.

M00 does not implement visual reconstruction. It creates the engineering environment in which later modules can be built safely.

## 2. Repository layout

```text
pixelperfect-studio/
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .editorconfig
├── .gitattributes
├── .gitignore
├── .npmrc
├── .node-version
├── .python-version
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── tsconfig.base.json
├── vitest.workspace.ts
├── pyproject.toml
├── uv.lock
├── .env.example
├── apps/
│   └── studio-cli/
├── packages/
│   ├── contracts/
│   ├── config/
│   ├── observability/
│   └── testing/
├── services/
│   ├── forensics/
│   ├── assets/
│   ├── compiler/
│   └── visual-qa/
├── workers/
│   └── cloudflare/
├── infra/
│   ├── supabase/
│   └── cloudflare/
├── schemas/
│   └── README.md
├── scripts/
│   ├── doctor.mjs
│   ├── validate-repo.mjs
│   ├── validate-skills.mjs
│   └── check-links.mjs
├── skills/
│   └── registry.yaml
├── .agents/
│   └── skills/
├── tests/
│   ├── fixtures/
│   ├── integration/
│   └── skill-evals/
├── docs/
│   ├── architecture/
│   ├── decisions/
│   ├── modules/
│   ├── runbooks/
│   ├── standards/
│   └── research/
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        ├── ci.yml
        ├── codeql.yml
        └── dependency-review.yml
```

The layout is created progressively. Empty service folders receive a `README.md` describing their future responsibility; they do not receive placeholder production code.

## 3. Root instructions

`AGENTS.md` is the repository-wide instruction source. It must define:
- project mission and module map
- source-of-truth ownership
- required planning and TDD workflow
- code style and naming rules
- contract-first change policy
- test commands and required verification
- asset licensing and provenance rules
- secrets and data-handling rules
- evidence requirements for claims
- module completion checklist
- when to load specialist skills

Module-specific `AGENTS.md` files may narrow or extend root instructions but may not weaken security, provenance, or verification requirements.

## 4. Package conventions

- `apps/` contains executable user-facing entry points.
- `packages/` contains shared libraries with explicit public exports.
- `services/` contains domain workers or bounded service implementations.
- `workers/` contains Cloudflare-specific runtime adapters.
- `infra/` contains migrations and infrastructure configuration, not runtime business logic.
- `schemas/` documents schema ownership; canonical schemas live in `packages/contracts/schemas/` to avoid duplication.
- `scripts/` contains repository maintenance and validation tools.
- `.agents/skills/` is the canonical cross-agent skill location.
- `skills/registry.yaml` lists all skills and their owner module, trigger, version, status, and evaluation location.

## 5. Required scripts

| Script | Input | Behavior | Exit behavior |
|---|---|---|---|
| `scripts/doctor.mjs` | Optional `--json` | Checks Node, pnpm, Python, uv, Git and required environment variable names without printing secret values | Nonzero only when a required local tool/version is missing; optional integrations report `not configured` |
| `scripts/validate-repo.mjs` | None | Checks required directories/files, package manifests, workspace membership, and forbidden generated paths | Nonzero on invariant failure |
| `scripts/validate-skills.mjs` | Optional skill path | Validates skill naming, `SKILL.md`, YAML frontmatter, trigger description, and relative links | Nonzero on invalid skill |
| `scripts/check-links.mjs` | Optional docs root | Checks local Markdown links and anchors; external links are not fetched in the default CI job | Nonzero on broken local links |

The scripts must expose importable pure functions so unit tests can verify behavior without spawning the entire toolchain. CLI entry points handle argument parsing and process exit codes only.

## 6. Environment variables

`.env.example` lists names and short descriptions only. Values must be empty placeholders or obvious non-secret examples.

Future variable groups:
- Supabase URL and public anon key for client-safe contexts
- server-only Supabase service role key
- Cloudflare account and R2 credentials
- AI provider keys
- observability endpoint and environment

M00 does not require any real value. The doctor must never print environment values.

## 7. GitHub workflows

### `ci.yml`

Run on pull requests and pushes to protected branches:
1. checkout source
2. install pinned Node and pnpm
3. install JavaScript dependencies with frozen lockfile
4. install pinned Python and uv dependencies from lockfile
5. run formatter checks
6. run lint and TypeScript type checks
7. run unit and contract tests
8. run repository and skill validation
9. run Markdown internal-link validation

### `codeql.yml`

Run on pull requests, protected branch pushes, and scheduled scans. Use the supported CodeQL setup for JavaScript/TypeScript and Python. Upload no source-derived secrets or private assets as workflow artefacts.

### `dependency-review.yml`

Inspect pull-request dependency changes for known advisories and configured license policy. Do not auto-approve dependencies.

## 8. Standards and templates

M00 must provide:
- architecture decision record template
- module specification template
- implementation plan template
- test strategy template
- runbook template
- incident report template
- asset provenance record template
- skill authoring and evaluation policy
- pull request template
- issue templates for bug, feature, research, and asset-source report

## 9. Skill governance

Skills are reusable operating procedures, not one-off project diaries. Each skill must have:
- unique kebab-case directory and matching frontmatter name
- precise `Use when...` trigger description
- one bounded responsibility
- inputs, outputs, assumptions, and failure handling
- evidence requirements and safety constraints
- one runnable or concrete example
- evaluation scenarios and expected behavior
- status: `draft`, `tested`, `verified`, or `retired`

A skill is not `verified` merely because its Markdown parses. Structural validation and behavioral evaluation are separate gates. New skills are created one at a time and evaluated before promotion.

Initial skill candidates are only registered, not yet authored:
- `reference-forensics`
- `layer-manifest-authoring`
- `asset-research-and-provenance`
- `asset-generation-review`
- `deterministic-reconstruction`
- `visual-regression-analysis`
- `design-memory-curation`
- `hybrid-knowledge-retrieval`
- `supabase-migration-safety`
- `cloudflare-job-orchestration`
- `figma-export-validation`
- `agent-task-orchestration`

## 10. Security baseline

- private repository until publication review is complete
- secret scanning and push protection enabled in GitHub settings
- dependency updates opened as reviewable pull requests
- no provider secret in browser bundles or client environment variables
- no service-role key in test fixtures, logs, screenshots, or documentation
- object storage private by default
- generated artefacts scrubbed for credentials and personal data before public release
- CI permissions reduced to the minimum required; prefer short-lived OIDC credentials for cloud access

## 11. Module 00 scope

### Included
- repository and directory conventions
- root agent instructions and contributor workflow
- runtime and package-manager pinning
- environment diagnostics and repository validators
- skill registry and skill structure validation
- Markdown link validation
- CI workflows and security baseline
- documentation templates and operating standards

### Excluded
- Supabase project creation or database migrations
- Cloudflare account, bucket, Worker, Queue, or Workflow creation
- live AI provider credentials or model calls
- computer-vision dependencies, model weights, or inference
- production reconstruction algorithms or UI
- Figma API integration

## 12. Module completion gate

M00 is complete only when:
- a clean checkout installs from pinned lockfiles
- `pnpm verify` exits successfully
- CI runs that same verification command
- each required script has unit tests including failure paths
- invalid skill fixtures fail and valid skill fixtures pass
- broken internal documentation links are detected
- `.env.example` contains no real credentials
- root and module instructions agree
- no external infrastructure or provider account was created

## 13. Deferred decisions

The following decisions belong to later module plans:
- exact image-processing and segmentation library versions
- model/provider selection and cost budgets
- exact database schema and RLS policies
- R2 bucket naming, retention, and lifecycle rules
- Queue and Workflow retry settings
- authentication and tenant isolation model
- final Figma export format
