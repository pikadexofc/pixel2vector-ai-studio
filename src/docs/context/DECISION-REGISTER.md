# Decision register

| ID | Decision | Current state | Historical note / rationale |
|---|---|---|---|
| DEC-001 | Build PixelPerfect Studio as a modular visual reconstruction and design-intelligence system | Confirmed | Not a prompt-only image generator |
| DEC-002 | Use separated probabilistic intelligence and deterministic production planes | Confirmed | Inference may propose; frozen inputs and compiler produce repeatable output |
| DEC-003 | Use a modular monorepo for the eventual platform | Confirmed in architecture brief | A private `pixelperfect-studio` repository was selected; no repository was created in this task |
| DEC-004 | Use Supabase PostgreSQL graph tables plus pgvector for structured memory and retrieval | Confirmed | A dedicated graph database is deferred until benchmarks justify it |
| DEC-005 | Use Cloudflare R2 for binary assets | Confirmed | Workers/Queues/Workflows are staged as orchestration needs mature; D1 is not selected |
| DEC-006 | GitHub stores versioned source; Notion is a human-readable knowledge interface | Confirmed | Avoid duplicate systems of record |
| DEC-007 | Use explicit evidence-backed trust levels NEW, TESTED, VERIFIED, CANONICAL | Confirmed | Agents cannot silently promote knowledge to CANONICAL |
| DEC-008 | Use root portable `plugin.json` targeting Agent Plugins 1.0.0 | Current OpenAI package decision | New official docs prefer root portable manifest; `.codex-plugin/plugin.json` is included only as compatibility fallback |
| DEC-009 | Ship this release as skills-only | Current plugin decision | No Supabase, R2, Figma, or provider credentials are configured; MCP would imply a hosted integration that does not exist |
| DEC-010 | Preserve exact-size reconstruction and independent QA evidence | Confirmed | Never call a result pixel-perfect without render and inspection |
| DEC-011 | Pixelmatch per-pixel threshold and overall mismatch ratio are separate measurements | Confirmed correction | Threshold is not the overall mismatched-pixel percentage |
| DEC-012 | Vibrant.js / ColorThief provide palette samples, not gradient geometry | Confirmed correction | Use spatial samples or fitted maps for gradients |
| DEC-013 | OCR detects strings and regions, not exact font identity | Confirmed correction | Font matching produces ranked candidates, not certainty |
| DEC-014 | html2canvas is not an editable Figma-layer exporter | Confirmed correction | Figma interoperability needs a separate mapping/import/export layer |
| DEC-015 | Editorial Neo-Brutalist Collage v1.1.0 is conditional | Confirmed preference | Use only when explicitly requested; it has Signal Collage, Transit Blue Editorial, and Quiet Typographic Event modes |
| DEC-016 | PixelPie visual identity should not be dominated by orange | Latest brand direction | Older orange-forward palette retained only as historical context; current direction is chromatic cyan/pink/magenta/blue with a dark base |
| DEC-017 | No external publication or infrastructure provisioning in this task | Explicit constraint | Package only; no push, publish, cloud create, or credential use |

## Retrieval ranking note

The previously discussed starting score is `S = 0.30V + 0.20G + 0.20C + 0.15Q + 0.10L + 0.05P`, where visual similarity, graph relevance, context compatibility, verified quality, licence suitability, and provenance reliability contribute. The weights remain hypotheses and must be benchmarked. Licence incompatibility and hard quality failures are rejection gates, not merely low ranking scores.


## 2026-11-03, user experience outranks usage metering

**Decision:** User task completion, continuity, and truthful delivery are P0. Usage metering, entitlement bookkeeping, reminders, analytics, and telemetry are best-effort P2 operations performed after delivery. They must not block, delay, interrupt, truncate, or discard an in-progress task.

**Reminder rule:** The Pickko baseline is 100 completed free cycles. Any eligible reminder is appended only after the answer and at most once every 20 minutes. If reminder state is unavailable or uncertain, skip the reminder and reconcile later.

**Fallback:** If a provider or integration fails, use an already-authorized alternative or continue manually in ChatGPT when the host remains available. Preserve progress and clearly mark unavailable verification.

**Rationale:** Optimize product behavior around the customer's completed job, not internal accounting accuracy. Do not promise unlimited external model capacity or funding; disclose genuine capacity limits and use the best available safe route.

**Source:** Explicit user direction in the 2026-11-03 conversation.


## 2026-11-03, product definition locked for production

**Decision:** PixelPerfect Studio is an image-to-editable-layered-HTML reconstruction engine. HTML is a fixed-size design artboard/document, not a responsive website. Every meaningful visual component must have its own stable layer identity. Distinct raster subjects are extracted or generated as separate PNG assets and embedded individually in the HTML.

**Customer output:** Exactly one final verified standalone HTML file. All intermediate files and production evidence remain internal.

**Quality priority:** Visual fidelity, independent component control, asset and typography quality, exact geometry and finishing outrank web performance, SEO, responsive behavior or app features.

**Rationale:** The original product brief and three reconstruction exercises show that the desired result is a properly separated design expressed in HTML, not a webpage wrapped around a screenshot.
