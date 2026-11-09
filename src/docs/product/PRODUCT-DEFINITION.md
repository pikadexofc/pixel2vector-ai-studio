# PixelPerfect Studio: Product Definition

**Version:** 1.0.0  
**Status:** Canonical product brief

## One-sentence definition

PixelPerfect Studio converts a flat visual reference into a high-fidelity, editable, fixed-size HTML design made from independently addressable visual layers and separately produced image assets.

## The product is a design reconstruction engine

The output format is HTML, but the product is not a website builder. The HTML acts as a structured design document or artboard. Its purpose is to preserve the visual composition while allowing meaningful components to be individually selected, inspected and edited in the HTML/CSS/SVG source. Raster subjects remain separate embedded image elements, not a single flattened image.

The product is optimized for visual fidelity, component separation, image quality, typography, masking, geometry and finishing. It is not optimized for responsive behavior, SEO, app functionality, interaction design, Lighthouse performance or mobile layout reflow.

## Core customer journey

1. Customer uploads a reference image.
2. The system inspects the original bytes and native normalized dimensions.
3. The system decomposes the composition into meaningful independent layers and groups.
4. Each layer receives a production method: source extraction, separate PNG generation, HTML/CSS, SVG or typography.
5. Source-specific image elements are extracted and masked before replacement is considered. If extraction cannot meet the visual requirement, a separate asset is generated, preferably one subject or visual role per PNG.
6. Typography is identified and tested. If the exact typeface is unavailable or visibly wrong, visible letterforms are extracted from the source and preserved as SVG paths or transparent raster artwork. This is not described as recovering the original font file.
7. A frozen layer manifest is compiled into a fixed-size artboard. Every meaningful component has its own stable layer identity.
8. All required PNG, SVG, font, texture and other resources are embedded individually into the standalone HTML. No external runtime dependency is allowed.
9. The actual HTML is rendered at the reference's normalized native dimensions, inspected in three passes, compared with the reference, corrected and revalidated.
10. Customer receives exactly one final verified standalone HTML file.

## What counts as an independent component

A component is independently layered when a designer could reasonably select, move, resize, hide, replace, recolour or edit it without rebuilding unrelated elements.

Examples:
- Background field or texture.
- Each photograph, isolated subject, product or illustration.
- Headline, subheading, caption and text block.
- Logo or wordmark.
- Decorative shape, divider, frame, line group or circuit illustration.
- Distinct foreground object, overlay, shadow or mask when it materially affects composition.

Do not over-fragment a visual into meaningless single pixels or thousands of trivial DOM nodes. Preserve logical grouping while keeping meaningful parts separately addressable. A complex photographic subject may remain one image layer; its independent shadow, frame or overlay can be separate if that improves control and fidelity.

## Asset policy

- Source extraction first for distinctive details that can be cleanly recovered from the supplied image.
- Generate separate PNG assets when original visual material is missing, occluded, inseparable, too low-resolution or unsuitable for clean extraction.
- Never generate the entire finished composition as the implementation asset.
- One independently meaningful subject or asset role per generated image, unless a grouped asset is genuinely inseparable.
- Use transparent backgrounds for isolated foreground objects when supported and visually appropriate.
- Inspect actual generated output for shape, crop, perspective, lighting, edge quality and resolution before use.
- Keep original inputs immutable and processed/generated derivatives separately identifiable.
- Embed assets as individual image layers in the final HTML. Internal files do not become additional customer deliverables.

## Typography policy

1. Recover and test the exact font where possible.
2. Compare real glyph shapes against the reference, not just font names.
3. If no exact match can be obtained, extract the visible letterforms from the reference.
4. Prefer SVG paths when vectorization preserves distinctive geometry; otherwise use transparent raster glyph artwork.
5. Preserve line breaks, baseline, scale, glyph proportions, kerning, tracking, slant, texture and distress.
6. Keep semantic text separately for accessibility and searchability where possible.
7. Do not claim extracted glyph artwork is an original font file.

## Artboard and implementation policy

- Fixed dimensions match the original normalized source dimensions unless the customer explicitly requests another canvas.
- Top-left origin and absolute pixel geometry are the default coordinate system.
- The layout is intentionally non-responsive. Viewing the file in a smaller browser window may scale the viewport, but must not rearrange or reflow the design.
- Use HTML/CSS for independently editable structure and effects, SVG for crisp vector detail, and embedded raster assets for photographic or texture-rich visual content.
- Use absolute positioning where composition fidelity requires exact placement. CSS Grid/Flexbox may organize internal groups when they do not distort the measured geometry.
- Do not flatten the entire source into a background image or screenshot.
- Prefer high-quality source and generated assets over aggressive file-size reduction. Do not downscale, quantize or recompress if it visibly degrades the reference match.
- The HTML must render offline with no remote images, fonts, scripts, stylesheets, data calls or relative runtime files.

## Quality policy

A valid HTML file is not automatically a valid reconstruction. The actual render must pass:

- Structural pass: dimensions, complete layer set, positions, order, clipping, masks, bounds, fonts and assets.
- Fidelity pass: typography, subject identity, crop, palette, texture, contrast, spacing, shape and composition.
- Finishing pass: edge quality, anti-aliasing, optical alignment, minor details, readable small copy and delivery integrity.

Record numerical metrics from matched source/render pairs. Use thresholds only when backed by a validated benchmark or a project-specific approved profile. Uncalibrated metrics are diagnostic, not objective pass/fail truth. Critical defects such as wrong canvas size, missing required content, missing assets, unreadable text, broken fonts or broken layer mapping must block delivery.

A final delivery must have actual render evidence, three recorded review passes, resolved critical defects, exact final HTML hash, verified offline asset/font loading and a successful delivery validator run. Do not claim pixel identity unless exact pixel equality is measured.

## Customer delivery rule

Exactly one customer-facing artifact is permitted: the final verified standalone `.html` file. All other artifacts remain internal, including manifests, generated/extracted PNGs, assets, prompts, font files, screenshots, crops, previews, difference maps, QA reports, source folders and ZIP archives.

If verification cannot be completed or a critical defect remains, do not provide an unverified HTML candidate. State the blocker briefly and continue the job when the required capabilities become available.

## Non-goals

- Responsive website construction.
- Web or app UI redesign from scratch unless explicitly requested as a separate task.
- SEO, analytics, forms, routing, databases or application behavior.
- Mobile-specific reflow or adaptive layouts.
- Motion and interactive effects not present in the reference.
- Delivering a source project bundle or a set of separate PNGs to the customer by default.
- Claiming guaranteed pixel-perfect output without measured evidence.

## Capability honesty

The plugin is a Skills-based agent workflow, not a bundled OCR engine, segmentation model, image generator, browser, rendering service or cloud backend. It must discover and use available host capabilities, explain a real blocker, preserve progress and never fabricate tool execution or QA evidence.
