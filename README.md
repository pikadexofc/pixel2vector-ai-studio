<p align="center">
  <img src="assets/icons/icon.svg" width="120" height="120" alt="Pixel2Vector AI Studio Logo" />
</p>

<h1 align="center">Pixel2Vector AI Studio</h1>

<p align="center">
  <strong>High-Fidelity AI Pixel-to-Vector Conversion & Live DOM-to-Illustrator Vectorizer</strong><br>
  <em>Engineered by Pickko • PixelPie Media</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg?style=flat-square" alt="License: MIT" /></a>
  <a href="https://github.com/pikadexofc/pixel2vector-ai-studio/releases"><img src="https://img.shields.io/badge/version-v1.0.0-blue.svg?style=flat-square" alt="Version 1.0.0" /></a>
  <a href="#"><img src="https://img.shields.io/badge/vector--integrity-100%25%20bezier%20math-purple.svg?style=flat-square" alt="Vector Math" /></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.10%20%7C%203.11-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python" /></a>
  <a href="#"><img src="https://img.shields.io/badge/node->=18.0-339933.svg?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node" /></a>
</p>

---

## ⚡ What is Pixel2Vector AI Studio?

**Pixel2Vector AI Studio** is a local-first, professional-grade **pixel to vector AI converter** and **DOM vectorization engine**. Designed for UI/UX designers, creative agencies, and developers, it bridges the gap between raster images (PNG, JPG, WebP), live web DOM trees, and mathematical vector formats (SVG, Adobe Illustrator `.ai`, EPS, PDF).

Unlike lossy heuristic auto-tracers or basic OCR tools, Pixel2Vector AI Studio computes **true cubic bezier polynomials** ($B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t)t^2 P_2 + t^3 P_3$), preserving typographic kerning, CSS bounding boxes, gradient angles, and border radii as distinct, editable vector layers.

---

## 🚀 Key Capabilities

### 1. 🎯 Neural Pixel-to-Vector AI Synthesis
* Convert pixel raster images (PNG, JPG, BMP) into resolution-independent SVG/AI paths.
* Multi-color palette segmentation with automatic edge anti-aliasing and noise suppression.
* Clean, non-overlapping vector geometry optimized for laser cutting, web animation, and print.

### 2. 🌐 Live DOM-to-Illustrator Extraction
* Rip any live webpage’s computed CSS box model and layout tree into grouped Adobe Illustrator (`.ai`) files.
* Powered by stealth CDP (Chrome DevTools Protocol) to capture dynamic Single Page Applications (SPAs) and complex CSS layouts without bot-detection interference.
* Extracts native SVG paths, CSS gradients, typography, and clip paths into organized Illustrator artboards.

### 3. 🎨 Tactile Local-First Studio GUI (`index.html`)
* Launch the included zero-dependency web console:
  * **Design Tokens Engine:** Extract and organize semantic color tokens, typography scales, and spacing ladders.
  * **UI Pattern Recipes:** Preview and test reusable vector layout patterns.
  * **Visual Memory Graph:** Track versioned brand assets and provenance metadata.

### 4. 🤖 Agentic Codex & Antigravity Plugin Skills
* Includes native skill modules for autonomous AI coding agents:
  * `deterministic-reconstruction`: Rebuild visual layouts with 1:1 pixel parity.
  * `asset-intelligence`: Automatically classify, compress, and bundle raster vs. vector assets.
  * `visual-reference-forensics`: Reverse-engineer design systems from raw reference screenshots.

---

## 📦 Architecture & Directory Layout

```
pixel2vector-ai-studio/
├── index.html                   # Tactile Studio GUI (Local-first web application)
├── package.json                 # Node manifest & scripts
├── pyproject.toml               # Python packaging & CLI entrypoints
├── LICENSE                      # MIT License (c) Pickko
├── README.md                    # Primary documentation & SEO schema
├── assets/
│   └── icons/                   # Full multi-resolution icon pack (16px to 1024px)
├── src/
│   ├── AGENTS.md                # Autonomous agent behavioral rules
│   ├── plugin.json              # Plugin manifest
│   ├── cli/                     # Command-line interface modules
│   ├── engine/                  # Bezier math & DOM vectorization core
│   ├── scripts/                 # Validation & packaging utilities
│   └── skills/                  # Autonomous design skills suite
└── docs/
    ├── LEARNINGS-AND-FIXES.md   # Defect resolution & architecture logs
    ├── OPERATING-RULES.md       # Evidence-backed operational rules
    └── STRUCTURED-LEARNING.json # Machine-readable test registers
```

---

## 🛠️ Quickstart

### Option A: Launch the Visual Studio GUI
Double-click `index.html` or serve locally:
```bash
npx serve .
# Or simply open index.html in any modern browser (Chrome, Brave, Edge, Firefox)
```

### Option B: Python CLI & Engine
```bash
# Clone the repository
git clone https://github.com/pikadexofc/pixel2vector-ai-studio.git
cd pixel2vector-ai-studio

# Install dependencies
pip install -e .

# Run pixel to vector conversion on an image
pixel2vector convert sample-logo.png --format svg --colors 16 --output logo.svg

# Rip a live web URL to Adobe Illustrator vector artboard
pixel2vector rip https://stripe.com --format ai --output stripe-hero.ai
```

---

## 🔍 SEO & Technical Keywords

* **Primary Intent:** pixel to vector ai, image to vector converter, raster to vector ai studio, html to vector illustrator, vectorizer ai alternative.
* **Secondary Intent:** svg converter ai, png to svg vector paths, dom to illustrator vector, web to vector extraction, auto trace ai alternative.

---

## 📄 License & Attribution

* **Author:** Pickko ([@pikadexofc](https://github.com/pikadexofc))
* **Organization:** PixelPie Media
* **License:** [MIT](LICENSE)

---

## 📊 Structured Schema Markup (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Pixel2Vector AI Studio",
  "operatingSystem": "Windows, macOS, Linux",
  "applicationCategory": "DesignApplication",
  "creator": {
    "@type": "Person",
    "name": "Pickko"
  },
  "offers": {
    "@type": "Offer",
    "price": "0.00",
    "priceCurrency": "USD"
  },
  "description": "High-fidelity AI pixel-to-vector converter, live DOM-to-Illustrator vectorizer, and design intelligence studio by Pickko.",
  "softwareVersion": "1.0.0",
  "featureList": [
    "Neural Pixel-to-Vector AI Synthesis",
    "Live DOM to Adobe Illustrator Extraction",
    "Cubic Bezier Spline Computation",
    "Local-First Studio GUI",
    "Autonomous Agent Plugin Architecture"
  ]
}
```

