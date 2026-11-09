# PixelPerfect Studio 0.2.3 release report

**Release date:** 2026-11-03  
**Package:** Skills-only portable Agent Plugin 1.0.0  
**Status:** Local package validated; desktop installation not yet exercised; not published.

## Product behavior changes

- Added `resources/PRODUCT-EXPERIENCE-CONTRACT.md` as the governing product rule for PixelPerfect Studio and Pickko AI.
- Established task completion, continuity, and truthful delivery as P0; quality as P1; metering, entitlement bookkeeping, reminders, analytics, and telemetry as P2.
- Made usage metering best-effort and non-blocking. A metering failure cannot stop, delay, interrupt, truncate, or discard an in-progress task.
- Preserved the current 100-free-cycle baseline. The answer is delivered first; an eligible reminder may appear only after delivery and at most once every 20 minutes. If reminder state is uncertain, skip the reminder.
- Added the governing product-priority reference to all 11 Skills and the root agent instructions.
- Updated the orchestrator, setup, manual continuity workflow, continuity contract, and fallback protocol to enforce the same rule.

## Installation changes

- Bumped both the portable root manifest and Codex compatibility manifest to `0.2.3`.
- Added `scripts/build_local_marketplace.py`, which creates a private personal-marketplace install bundle.
- Added `Install-PixelPerfectStudio.ps1` to the generated bundle. It backs up an existing PixelPerfect folder, installs the new plugin folder, and merges the marketplace entry while preserving other entries.
- Added Windows installation documentation. The install bundle does not publish the plugin or connect external services.

## Verification

- Plugin validator: **PASS**, 11 Skills, 93 package files, four declared brand asset paths.
- Schema/example validation: **PASS**, portable manifest and seven typed examples, 8/8.
- Unit tests: **PASS**, 18/18.
- Canonical plugin ZIP: built twice and compared byte-for-byte.
- Personal marketplace ZIP: built twice and compared byte-for-byte.
- Clean plugin ZIP extraction: plugin validator and schema/example checks passed.
- Clean marketplace extraction: manifest path, plugin version, and installer presence checked.
- ZIP CRC integrity: passed for both bundles.

## Not executed

- The Windows PowerShell installer was not run because this host has no PowerShell runtime.
- ChatGPT desktop local marketplace import and fresh-chat invocation were not tested. The current chat is on Android and cannot write into the user's Windows profile.
- Public Plugin Directory submission, review, approval, and publication were not attempted.
- No cloud resources, databases, integrations, billing, or remote services were changed.

## Product boundary

The package remains skills-only. It provides instructions, references, schemas, examples, validation tools, a deterministic packager, and checkpoint utilities. It does not include a deployed visual reconstruction engine, backend API, MCP service, browser interface, automatic provider failover, or app-level offline persistence. The manual ChatGPT fallback is Skill guidance and works only while ChatGPT and the required host capabilities remain available.
