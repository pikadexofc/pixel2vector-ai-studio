# PixelPerfect Studio improvement research

**Research date:** 2026-11-03  
**Baseline:** PixelPerfect Studio 0.2.0  
**Scope:** visual analysis fidelity, reference reconstruction, QA, asset intelligence, agent workflow, memory, and plugin architecture  
**Decision status:** research recommendations, not implementation approval

## Executive finding

PixelPerfect Studio has a useful workflow contract, but its current package is primarily an instruction and validation product. Its Python scripts validate examples, validate the plugin, and build deterministic ZIP files. They do not yet perform computer vision, OCR, segmentation, image registration, screenshot rendering, perceptual comparison, or automatic defect localization.

The highest-value improvement is therefore not to add many more agent roles. It is to create a repeatable visual-evidence loop:

`reference → normalized source → multi-scale analysis → measured layer graph → deterministic render → multi-metric comparison → localized defect diagnosis → targeted repair → verified render`

The agent should reason and propose. Deterministic tools should measure, transform, render, compare, and report. The same frozen inputs should reproduce the same render and QA result.

## 1. Current package audit

The inspected 0.2.0 package contains:

- 10 Skills and their supporting references.
- Portable Agent Plugins 1.0.0 root `plugin.json` plus `.codex-plugin/plugin.json` compatibility fallback.
- 7 JSON Schemas, 6 example records, resources, installation guidance, and context/decision registers.
- A Python validator, example validator, deterministic packager, and 5 passing unit tests.

The current QA reference already correctly separates Pixelmatch's per-pixel threshold from the global mismatch ratio, recommends region weighting, preserves rendering metadata, and requires structural, fidelity, and finishing passes.

### Main gaps found

| Gap | Consequence | Priority |
|---|---|---|
| No executable visual-analysis engine | Geometry, OCR, masks, colors, and gradients are not measured by packaged code | P0 |
| No standardized golden benchmark | There is no evidence that a prompt, model, or workflow change improves fidelity | P0 |
| No calibrated composite metric | A single score can hide missing text or incorrect layout behind a large matching background | P0 |
| QA has no full defect-to-layer attribution pipeline | Agents may change the wrong layer or regenerate too much | P0 |
| No deterministic renderer profile | Browser, fonts, colour management, and device scale can create false diffs | P1 |
| Typography is candidate-oriented but not systematically evaluated | Font fallback, weight, tracking, line wrapping, and text geometry can drift | P1 |
| Asset search is not backed by a working, indexed candidate corpus | Similarity and provenance are described but not executed | P1 |
| Memory model is architectural only | No actual Supabase/R2/pgvector ingestion and retrieval is active | P2 |
| Figma mapping is conceptual | No live node round-trip or geometry verification is active | P2 |
| No measured cost/latency policy | Heavy models may be used where cheap deterministic tools would suffice | P1 |

## 2. What research implies

### 2.1 Use divide-and-conquer visual analysis

Large references should be read at multiple scales. Start with the whole composition, then divide it into meaningful regions, then inspect high-resolution crops for text, edges, masks, and small details. Overlapping crop boundaries prevent elements at tile edges from being lost. A global pass alone can miss small type and local alignment. A crop-only approach can lose the hierarchy and relationships between regions.

DCGen reports up to 15% improvement in visual similarity and 8% in code similarity for large screenshot-to-UI inputs using segment-aware generation and reassembly. This is evidence for testing hierarchical analysis, not a guaranteed improvement for posters, logos, or every design category.

### 2.2 Build a complementary metric stack

No single image metric captures exact visual reconstruction:

| Signal | What it measures | Use | What it cannot prove |
|---|---|---|---|
| Exact pixel difference / mismatch ratio | Pixel-level raster equality or deviation | Exact output, anti-aliasing, local shifts | Semantic equivalence; it is sensitive to rasterization noise |
| SSIM / MS-SSIM | Local structural similarity | Layout and structure regression | Correct text content or semantic correctness |
| LPIPS | Deep-feature perceptual distance | Perceptual appearance changes | Exact position, copy, font identity, or colour values |
| DISTS | Structure and texture similarity | Textured artwork and image regions | Correct text or exact geometry |
| DreamSim | Holistic human-aligned visual similarity | Composition-level ranking and candidate retrieval | Exact coordinates or character-perfect text |
| DINOv2 dense features | Local visual correspondence and feature similarity | Match reference regions to rendered regions; help locate moved or substituted content | Exact colour or text equality |
| OCR metrics | Text recognition and bounding-box agreement | Required copy, line order, text region location | Exact typeface identity |
| Geometry metrics | Bounding-box IoU, centre displacement, baseline, edge and mask overlap | Element placement and shape accuracy | Overall artistic quality |
| CIEDE2000 / ΔE00 | Perceptual colour difference in Lab | Palette, fills, gradients, and colour-critical regions | Composition or shape accuracy |

Use the metrics as independent diagnostic channels. Never allow a high holistic similarity score to compensate for missing required text, wrong canvas dimensions, an omitted logo, or a mispositioned critical element.

### 2.3 Make segmentation and detection complementary

- OCR should propose text strings, word/line boxes, reading order, language, and confidence.
- An open-vocabulary detector such as Grounding DINO can propose text-conditioned object boxes.
- SAM 3 can segment repeated visual concepts from text or visual prompts. SAM 2 remains a documented fallback for point/box/mask prompted segmentation.
- Edge, contour, connected-component, and line detection should handle geometric artwork, rules, frames, and primitive shapes that object segmenters may not classify well.
- Keep original masks and probabilities. Boxes are derived summaries, not replacements for masks.
- Preserve occlusion and parent-child relationships. A flat list of boxes cannot fully describe overlapping design layers.

Do not apply semantic segmentation to every pixel by default. Use it only where a region needs separation, alpha extraction, object identification, or asset matching. For flat vector artwork, contour and colour-region analysis may be more precise and much cheaper.

### 2.4 Treat typography as its own forensic domain

OCR gives text and location, not a reliable exact font name. Analyse text in this order:

1. Exact copy and reading order.
2. Line/block bounds and baseline positions.
3. Font size, weight, width, line-height, tracking, alignment, and case.
4. Glyph-shape features and ranked font-family candidates.
5. Render candidate fonts with the actual copy and compare width, wrapping, and glyph contours.
6. Confirm exact font only from source metadata, supplied font files, or strong reproducible evidence.

Pin font files and browser font loading for final screenshots. A font substitution can alter width and line wrapping even when the nominal CSS size is unchanged.

### 2.5 Use visual feedback as a closed loop

A high-fidelity agent should not stop after generating HTML or SVG. It should render the output, compare it with the reference, inspect difference regions, identify the affected layer IDs, edit only those layers, and render again. VisRefiner studies learning from rendered visual differences. UI2Code research also frames screenshot-to-code as an interactive visual optimization problem rather than a one-shot generation task.

Adopt this workflow without claiming that the research model itself is bundled or that an external method's reported benchmark gain transfers directly to PixelPerfect Studio.

## 3. Recommended analysis pipeline

### Stage A: immutable intake and normalization

- Preserve the original byte-for-byte and compute SHA-256.
- Record format, dimensions, alpha, EXIF orientation, ICC profile, bit depth, and metadata.
- Create a normalized analysis derivative with recorded orientation and colour-space transforms.
- Use the normalized pixel coordinate system for all detections; store the exact inverse transform to original coordinates.
- Never resize or crop the source silently.

### Stage B: global composition analysis

- Determine canvas, aspect ratio, dominant regions, safe margins, primary axis, and major alignment landmarks.
- Identify visual hierarchy: dominant object, title, secondary copy, imagery, supporting marks, and background.
- Record confidence and evidence for each observation.

### Stage C: region and layer discovery

- Create a hierarchical region tree.
- Run detection/OCR/segmentation only where useful.
- Capture bounding boxes, masks, polygons, line baselines, z-order hypotheses, occlusion, crop, and negative space.
- Keep `OBSERVED`, `DERIVED`, `ESTIMATED`, and `UNKNOWN` separate.
- Record model/tool version, prompts, thresholds, and evidence references.

### Stage D: specialised measurements

- Geometry: landmark distances, relative alignment, bbox IoU, centre shift, aspect ratio, edge overlap, and mask IoU.
- Typography: transcription, word/line boxes, baselines, line wrapping, font candidates, and rendered width.
- Colour: sample locations and Lab values; estimate gradients from spatial samples, not a single palette list.
- Assets: source identity, visual similarity, crop/scale, transparency, licence, and provenance.

### Stage E: manifest-first deterministic compilation

- Freeze the layer manifest, source assets, fonts, design tokens, and renderer version.
- Compile a fixed-size artboard with stable layer IDs.
- Give every rendered DOM/SVG layer a persistent `data-layer-id` or equivalent mapping.
- Preserve exact canvas dimensions and top-left pixel coordinates.
- Keep asset variants connected to immutable originals.

### Stage F: controlled rendering

Pin Chromium/Playwright version, viewport, device scale factor, colour scheme, timezone/locale where relevant, fonts, image decoding, animation state, and all resource hashes. Wait for `document.fonts.ready` and decoded image assets. Disable motion and time-dependent content. Render exact dimensions with no silent fit-to-screen scaling.

### Stage G: multi-channel visual QA

Produce:

- Raw and thresholded pixel diff maps.
- SSIM and optional multi-scale SSIM.
- Optional LPIPS/DISTS/DreamSim measurements on appropriate image regions.
- DINOv2 patch correspondence/region matching when local feature diagnosis is needed.
- OCR text and geometry comparison.
- Geometry, edge, and mask overlap measures.
- Region-wise colour difference maps.
- Connected components and defect candidates mapped to manifest layer IDs.

Keep an unwarped score as the primary score. Registration tools such as OpenCV ECC can diagnose capture shifts or identify an environmental mismatch, but must not warp the primary output before scoring. Doing so could hide a genuine layout error.

### Stage H: defect-guided repair

Classify each defect as one or more of:

`missing`, `extra`, `translation`, `scale`, `rotation`, `crop`, `z_order`, `mask`, `shape`, `font_family`, `font_weight`, `font_size`, `line_wrap`, `baseline`, `tracking`, `colour`, `gradient`, `shadow`, `opacity`, `blend_mode`, `render_environment`.

For each defect retain evidence, affected layer IDs, severity, confidence, recommended change, and a verification method. Correct the smallest affected layer set. Re-render and verify the same defect region and its neighbouring regions for regressions.

## 4. Candidate tool stack

The stack below is a candidate set for comparative tests, not a requirement to install every package in every environment.

| Function | Candidate | Placement |
|---|---|---|
| Image metadata, EXIF and raster transforms | Pillow / libvips (Sharp on Node.js) | Deterministic local engine |
| Geometry, contours, ECC registration, colour conversion | OpenCV | Deterministic local engine |
| OCR and text-region parsing | PaddleOCR 3.x / PP-OCRv6; compare with another OCR provider on the test corpus | Optional analysis adapter |
| Open-vocabulary detection | Grounding DINO | Optional model adapter |
| Prompted segmentation | SAM 3, with SAM 2 fallback where needed | Optional model adapter |
| Dense visual correspondence | DINOv2 | Optional feature extractor |
| Structural similarity | scikit-image SSIM / MS-SSIM implementation | Deterministic QA |
| Perceptual distance | LPIPS, DISTS, DreamSim | Optional QA model adapters |
| Browser rendering | Playwright with pinned Chromium | Deterministic renderer |
| DOM/layout geometry | Browser bounding-box and computed-style capture | Deterministic renderer |
| Raster difference | Pixelmatch or an equivalent pinned implementation | Deterministic QA |
| Design tokens | DTCG Format Module 2025.10 | Interoperability format |

### Selection rules

- Benchmark OCR on supplied languages and typography conditions before selecting a default.
- Test model availability, hardware, licence, installation size, latency, and inference cost before adopting a vision model.
- Keep each model behind an adapter. Store provider, model/checkpoint, version, input resolution, threshold, and inference parameters in every result.
- Keep model weights out of the portable Plugin ZIP unless they are small, redistributable, licensed, and necessary. Prefer separately installed engine dependencies or an explicitly hosted MCP service.
- Do not represent any candidate tool as active until it is installed and exercised.

## 5. A calibrated fidelity score, not an arbitrary score

Use hard gates plus a per-category scorecard. A proposed pilot score is:

`VFS = 0.25G + 0.20T + 0.15A + 0.15C + 0.10E + 0.15P`

Where each component is normalized to 0–100:

- `G`: geometry and layout fidelity.
- `T`: required text, OCR, typography, and line-layout fidelity.
- `A`: asset identity, crop, scale, and mask fidelity.
- `C`: regional colour and gradient fidelity.
- `E`: edge, contour, and fine-detail fidelity.
- `P`: multi-scale perceptual fidelity from suitable perceptual metrics.

These weights are **initial hypotheses only**. They are not empirically validated and should not become a public quality promise. Create separate profiles for poster/editorial, UI screenshot, logo/icon, and photographic/composite work, then fit weights to expert pairwise judgments.

Hard gates override the composite:

- Exact requested canvas size and orientation.
- No missing or extra critical layer.
- Required text matches exactly unless the user permits a copy change.
- No unapproved substitution of a logo, face, product, or licensed asset.
- No clipping/overflow or broken asset in the required delivery area.
- Provenance/licence state known for sourced external assets.

## 6. Benchmark and evaluation plan

Build a task-specific PixelPerfect Reference Reconstruction Benchmark. Design2Code is a useful external reference for web UI screenshot reconstruction, but its 484 webpage cases are not representative of posters, logos, editorial art, or social creatives. Do not reuse its headline scores as PixelPerfect performance claims.

### Pilot corpus

Start with 24 rights-cleared references, four each from:

1. Posters and flyers.
2. Social advertisements and campaign creatives.
3. Editorial and typographic compositions.
4. Web/app screenshots.
5. Icons, logos, and vector marks.
6. Image composites with masks, overlays, or complex crops.

For each case capture the original, normalized dimensions, reference hash, ground-truth or reviewed region boxes, required copy, known assets and licences, layer manifest, renderer profile, human review, and baseline render.

Expand to at least 60 varied examples before claiming robust improvements. Maintain a held-out test set and do not tune prompts against all test fixtures.

### Evaluation protocol

- Compare the current 0.2.0 workflow with each candidate improvement on the same cases.
- Use at least two independent design reviewers for a sample of pairwise A/B comparisons.
- Blind the reviewers to method identity.
- Record pairwise preference, defect severity, and dimension-specific ratings.
- Report correlation between automated metrics and human judgments by design category.
- Track critical-defect false negatives, repair success, regressions, time, tool cost, and failure/abstention rates.
- Keep the benchmark fixtures and metric versions pinned.

### Provisional release targets

These are target values for the pilot, not measured results:

- Critical region bbox IoU: ≥0.90 on annotated primary regions.
- Required copy: zero character errors for text the brief marks exact.
- No hard-gate violations on accepted releases.
- Automated score ranking should reach Spearman correlation ≥0.70 against reviewer rankings before using the score to gate releases.
- At least 70% of paired reviewers prefer the new workflow over 0.2.0 on the held-out pilot set.
- Every changed layer must have a before/after render and regression check.

Adjust these after reviewing annotation noise and inter-rater agreement. A benchmark target is not a claim that the current system meets it.

## 7. Plugin and platform architecture

Keep the portable Plugin skills-only while no hosted analysis service exists. Its Skills can orchestrate host-native image/file/Python capabilities when the current host exposes them; the Plugin cannot grant those tools or install model weights by itself.

Build the deterministic visual engine as a separately testable package/CLI. If ChatGPT needs guaranteed remote computation, expose the engine through a real, secured MCP service and then move the Plugin to a deliberately designed hybrid architecture. That change requires a separate service, hosting, authentication, privacy, security, and operational review.

Recommended split:

- **Plugin layer:** task routing, evidence requirements, approvals, workflows, and portable skills.
- **Forensics engine:** image intake, normalization, OCR, geometry, color, masks, and feature extraction.
- **Composition engine:** layer-manifest validation, SVG/HTML/CSS compilation, and fixed-size rendering.
- **QA engine:** deterministic diffs, metrics, defect localization, and report generation.
- **Memory service:** Supabase/Postgres metadata and relationships, pgvector retrieval, R2 binary storage, GitHub source history, and Notion documentation when actually provisioned.

No cloud resource should be treated as active until provisioned, connected, tested, and recorded in the source register.

## 8. Prioritized improvement scope

| Order | Work package | Priority | Why it comes first | Exit evidence |
|---:|---|---|---|---|
| 1 | Evaluation corpus, annotation contract, and metric scorecard | P0 | Without this, improvements cannot be measured | 24 pilot fixtures; gold regions/copy; baseline report |
| 2 | Image intake and normalization CLI | P0 | All downstream coordinates depend on stable inputs | Orientation/ICC/alpha/hash tests; round-trip coordinate tests |
| 3 | Multi-scale reference forensics | P0 | Improves element recall and reduces missed details | Region/crop report, OCR + geometry confidence, coverage audit |
| 4 | Deterministic renderer profile and DOM-to-layer map | P0 | Makes render comparisons reproducible and defects actionable | Same-source repeat renders with environment manifest and stable IDs |
| 5 | Multi-metric QA and defect localization | P0 | Establishes measurable fidelity and smallest-scope fixes | Pixel/SSIM/geometry/OCR/colour report with per-layer defect map |
| 6 | Defect-guided repair loop | P1 | Converts analysis into actual iterative quality gains | Controlled A/B improvement, zero new hard-gate regressions |
| 7 | Typography, gradients, and complex mask analysis | P1 | These frequently dominate perceptual mismatch | Font candidate report, regional ΔE, mask/edge metrics |
| 8 | Asset retrieval and provenance index | P1 | Better assets improve composition more than prompt tweaking | Rights-filtered retrieval test set, crop/identity review |
| 9 | Cost-aware model routing and confidence calibration | P1 | Uses heavy models only when needed | Cost/latency/fidelity curves and abstention checks |
| 10 | Persistent memory ingestion and Figma round-trip | P2 | Depends on verified outputs and actual service connections | Live integration tests with read/write boundaries |

## 9. Non-goals and safety constraints

- Do not claim pixel-perfect from a text-only analysis.
- Do not use one global embedding or composite score as the sole pass/fail gate.
- Do not resize or register the primary output to hide errors.
- Do not infer exact font identity from OCR alone.
- Do not treat asset similarity as licence permission.
- Do not send private/client reference images to a third-party model without an appropriate user-approved data path.
- Do not add a second vector database or graph database before measured need.
- Do not package unreviewed model weights, credentials, or remote-code execution.
- Do not claim the plugin has connected Supabase, R2, Notion, GitHub, or Figma when it has not.

## 10. Research references

1. OpenAI, Package your plugin: https://developers.openai.com/plugins/build/plugins
2. OpenAI, Upload and submit your plugin: https://developers.openai.com/plugins/deploy/submission
3. Design2Code, NAACL 2025: https://aclanthology.org/2025.naacl-long.199/
4. DCGen, Divide-and-Conquer: Generating UI Code from Screenshots: https://doi.org/10.1145/3729364
5. VisRefiner, Learning from Visual Differences for Screenshot-to-Code Generation (2026): https://arxiv.org/abs/2602.05998
6. UI2Code^N, UI-to-Code Generation as Interactive Visual Optimization (2026): https://proceedings.mlr.press/v306/yang26v.html
7. LPIPS, The Unreasonable Effectiveness of Deep Features as a Perceptual Metric, CVPR 2018: https://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_The_Unreasonable_Effectiveness_CVPR_2018_paper.html
8. DISTS, Image Quality Assessment: Unifying Structure and Texture Similarity: https://pubmed.ncbi.nlm.nih.gov/33338012/
9. DreamSim, NeurIPS 2023: https://papers.neurips.cc/paper_files/paper/2023/hash/9f09f316a3eaf59d9ced5ffaefe97e0f-Abstract-Conference.html
10. Meta DINOv2 repository and dense matching demos: https://github.com/facebookresearch/dinov2 and https://dinov2.metademolab.com/demos
11. Meta SAM 3: https://ai.meta.com/research/sam3/
12. Meta SAM 2: https://ai.meta.com/research/sam2/
13. Grounding DINO: https://github.com/IDEA-Research/GroundingDINO
14. PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
15. OpenCV ECC image alignment: https://docs.opencv.org/doc/doxygen/html/dc/d6b/group__video__track.html
16. scikit-image SSIM API: https://scikit-image.org/docs/stable/api/skimage.metrics.html
17. W3C Design Tokens Community Group, Format Module 2025.10: https://www.designtokens.org/tr/2025.10/

## Decision requested before implementation

Approve the P0 work packages as a separately testable visual-engine phase. Keep the portable Plugin architecture skills-only until a real local engine or hosted MCP server exists. Do not create new Skills or declare new integrations merely to make the package appear more capable.
