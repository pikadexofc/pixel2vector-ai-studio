---
name: design-system-architecture
description: Use when translating recurring visual preferences into design tokens, typography systems, reusable components, brand rules, or project-specific visual modes.
---

# Design System Architecture
## Governing product priority

Follow `resources/PRODUCT-EXPERIENCE-CONTRACT.md`. **User task completion comes first. Usage metering is best-effort and must not block or interrupt the current task.** Deliver first, reconcile usage and reminders afterward, and use manual ChatGPT continuation when an integration fails.

Turn visual preferences into explicit, reusable constraints without forcing one aesthetic onto every project. Keep a distinction between user preferences, brand-specific rules, and the current project brief.

## Decision hierarchy

1. Explicit current project brief.
2. Latest confirmed brand/system decision for the named brand.
3. Relevant remembered design preferences.
4. Reusable pattern library, only when requested or contextually appropriate.
5. Generic defaults, clearly identified as proposals.

A current explicit brief overrides older remembered preferences. Never silently activate a named style system because it exists in memory.

## Relevant visual preferences

- Contemporary, minimal, high-contrast, deliberate composition.
- Dark/charcoal bases, soft white, and selective cyan or chromatic accents where the project allows.
- Avoid cartoonish, noisy, gratuitous cyberpunk, graffiti, heavy textures, and unnecessary neon effects.
- Use glassmorphism or cinematic lighting only when it supports hierarchy and legibility.
- Typography should carry hierarchy and rhythm; do not add decoration to compensate for weak information structure.
- Do not default to cards or icons when direct composition or typography is clearer.

## PixelPie Media context

The current agency direction moved away from orange-dominant branding toward chromatic cyan, pink, magenta, and blue on a dark base. The older orange palette is historical and should not dominate current brand work. The PixelPerfect Studio plugin's current dark/cyan palette is its own provisional product identity, not a full replacement for all PixelPie brand assets.

## Conditional style system

Editorial Neo-Brutalist Collage v1.1.0 is a separate, conditional design system. Activate it only when the user explicitly requests it or names it. It contains three modes:
- Signal Collage: canonical violet/yellow palette.
- Transit Blue Editorial: blue-led editorial mode.
- Quiet Typographic Event: restrained typographic mode.

Do not apply it automatically to unrelated projects.

## Token workflow

1. Extract roles before choosing values: background, surface, text, muted text, accent, border, focus, semantic status, spacing, typography, radius, shadow, and motion.
2. Name tokens semantically; keep component tokens separate from primitive values.
3. Preserve light/dark theme semantics when the target needs both.
4. Store tokens in a machine-readable design-token format and maintain source/approval metadata.
5. Avoid duplicating token systems by project where a shared brand system is already defined. Use explicit project overrides.
6. Validate contrast, typography hierarchy, and component state coverage.

## Output

Deliver token tables or DTCG-compatible JSON, typography scales, component rules, theme modes, style activation rationale, and any unresolved brand decisions. See [design preferences](references/DESIGN-PREFERENCES.md).

## Service failure fallback

Never abandon the user's design job or ask them to repeat requirements already present in the conversation. If an integration, provider, renderer, storage system, or required host tool is unavailable, route to `manual-fallback-continuity`. Continue in the current ChatGPT conversation with accessible inputs and available host capabilities, preserve completed outputs, and create or update the portable continuity checkpoint. Mark unavailable automation and verification honestly; never fabricate OCR, segmentation, rendering, numerical QA, upload, database, Figma, or deployment results. If ChatGPT itself is unavailable, preserve local project files and the checkpoint for later resumption.


## PixelPerfect customer delivery boundary

For reconstruction jobs, preserve working tokens, mappings, source data, implementation files and validation evidence internally. The only default customer-facing deliverable is one final verified standalone HTML file. Do not attach previews, manifests, assets, reports, project folders or ZIP bundles. If the final HTML acceptance gate cannot pass, do not provide an unverified candidate.


## Typography evidence and recovery

For reconstruction jobs, do not select a lookalike font before attempting exact font identification. Compare rendered glyphs, not names alone. If the exact font is unavailable or visibly mismatched, use source-derived glyph artwork: clean a mask and vectorize to SVG paths where practical, otherwise keep transparent raster glyphs. Preserve proportions, spacing, tracking, kerning, baseline, line breaks and distinctive distress. Keep semantic text separately for accessibility. Record whether the result is a verified font, extracted glyph art, an approved substitute or unknown.

The extraction/forensics artefacts remain internal. Reconstruction customers receive only the final verified standalone HTML.
