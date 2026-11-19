# Pixel2Vector Studio

A fresh, mobile first, voice guided workspace for turning raster artwork into editable vector files.

## Frontend

The current application entry point is the standalone root `index.html`. It introduces a new product experience rather than carrying forward the previous dashboard styling.

The interface includes:

- Responsive mobile and desktop layouts, designed around phone sized screens first.
- Drag and drop image input and local file preview.
- Local image inspection for native dimensions and sampled dominant colors.
- Plain language command input and browser speech recognition where supported.
- Contextual style choices and optional advanced controls.
- An agent workflow presentation with clear stages and honest status.
- Optional haptic feedback using the browser Vibration API or a native Capacitor Haptics bridge.
- Reduced motion, keyboard focus, and touch sized primary controls.
- A clearly labelled sample SVG workflow.

## Run locally

Open `index.html` in a modern browser, or serve the repository:

```bash
npx serve .
```

Microphone access requires a supported browser and a secure context. Haptic output depends on device and browser support. The interface remains usable with typing and visual feedback when either capability is unavailable.

## Current integration boundary

This branch contains the new frontend and its local image inspection flow. It does **not** contain a production vectorization engine connected to this interface. The guided four stage run and sample SVG are explicitly demonstrations. Uploaded user images are not sent to the repository's legacy `/api/vectorize` placeholder endpoint.

Before enabling real conversion, connect a verified raster to vector engine, progress reporting, error handling, and real SVG/EPS/PDF exporters. Do not present a sample asset as a conversion of a user's upload.

## Branch

The mobile voice first implementation is maintained on `feature/mobile-voice-first-studio`. The existing `main` branch is unchanged.
