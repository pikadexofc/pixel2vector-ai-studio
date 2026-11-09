---
name: workspace-engineering
description: Use when inspecting or changing a local project, repository, plugin package, scripts, documentation, or generated files as part of PixelPerfect Studio work.
---

# Workspace Engineering
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Use host-native workspace capabilities and respect the user's authorization. This Skill describes operating policy; it does not grant filesystem, shell, Python, browser, or GitHub access.

## Capability routing

- `read`: known file or exact range.
- `list`: directory shape and file inventory.
- `search`: broad semantic/content discovery.
- `grep`: exact terms, symbols, identifiers, or regex.
- `patch`: focused edit to existing content.
- `write`: create or replace a file when authorized.
- `shell`: run repository commands, tests, Git inspection, or archive tooling.
- `python`: deterministic parsing, transformations, hashing, and validation.

Use the narrowest operation that fits. Discovery defaults to read-only. Mutation includes write, patch, delete, move, rename, format, and mutating shell commands.

## Engineering loop

1. Inspect repository instructions and current state before editing.
2. Read project design/spec and the implementation plan.
3. Isolate work in a branch/worktree when the host supports it and the user has authorized it.
4. For code changes, write a failing test first, run it, implement the minimum, run it again, then run the complete relevant suite.
5. For new Skills, test the instruction structure and run behavioural evaluation cases; do not call a Skill verified solely because YAML parses.
6. Inspect diffs and generated files; do not overwrite unrelated user work.
7. Validate package paths, secrets, symlinks, binary assets, and archive content.
8. Build deterministic artefacts twice and compare hashes when determinism is part of the contract.
9. Extract the ZIP to a clean temporary directory and validate the extracted copy.
10. Report exact files, executed commands, pass/fail counts, skipped checks, hashes, and limitations.

## Safety and provenance

- Never expose or package credentials, tokens, private data, or unrelated user files.
- Inspect untrusted scripts before running them.
- Do not execute arbitrary repository code without understanding side effects.
- Do not publish, push, deploy, create cloud resources, or mutate connected accounts unless explicitly authorized.
- Read-only GitHub repository evidence does not imply source-code audit. Label README-only findings as such.
- Preserve third-party source/licence data and user-provided original assets.

## Verification language

Say `executed` only when a host execution tool returned evidence in the current task. Say `static review` when you only inspected source. Say `not tested` for unexecuted behaviour. Never convert an absent tool into an invented result.

See [host tool boundaries](references/HOST-TOOL-BOUNDARIES.md).

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.


## PixelPerfect customer delivery boundary

For reconstruction jobs, preserve working tokens, mappings, source data, implementation files and validation evidence internally. The only default customer-facing deliverable is one final verified standalone HTML file. Do not attach previews, manifests, assets, reports, project folders or ZIP bundles. If the final HTML acceptance gate cannot pass, do not provide an unverified candidate.
