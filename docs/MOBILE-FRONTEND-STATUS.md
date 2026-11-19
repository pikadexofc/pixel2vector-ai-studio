# Mobile Voice First Frontend

## Product direction

A new mobile first creative instrument, not a restyle of the previous dashboard. The core interaction is simple:

1. Add an image.
2. Describe the desired result in ordinary language or with a few visual choices.
3. Let the system inspect the source and prepare a transparent workflow.
4. Review the result before export.

The interface uses a warm mineral canvas, deep botanical green, and vermilion actions. Animated vector geometry communicates the product's purpose. This is a new product direction; no previous dashboard or supplied style system was copied as the visual template.

## Implemented in the frontend

- Responsive layout tested at 320, 360, 390, 430, 768, 1024, and 1440 pixel widths.
- Image selection, drag and drop, source preview, and file size guard.
- Browser local image inspection for dimensions and sampled color groups.
- Voice input through the Web Speech API where available.
- Typed command parsing for color count, edge cleanup, smoothing, background removal, layers, and navigation.
- Optional spoken confirmation.
- Optional event based haptics. The adapter checks a native Capacitor Haptics bridge first, then the browser Vibration API. Unsupported devices retain visual feedback.
- Advanced color and edge controls are progressive disclosure.
- Reduced motion preference and keyboard focus support.
- Explicit sample workflow and sample SVG export.

## Honest capability boundary

The interface currently stops after local image inspection. It does not claim to produce a vector from the uploaded image. The guided animation and sample SVG are marked as demonstrations.

The existing repository endpoint `/api/vectorize` is a placeholder response, so this frontend intentionally does not call it.

## Next integration requirement

Connect a real production vectorization engine that accepts the source image and selected options, returns a job identifier and exposes progress, result artifacts, errors, and cancellation. Then connect the existing stage interface to actual backend events. Enable SVG, EPS, and PDF downloads only when backed by verified outputs.

## Verification

The HTML was exercised in headless Chromium at mobile and desktop sizes. The tests covered settings navigation, voice panel opening and closing, typed command parsing, image upload and preview, local image analysis, color sampling, sample workflow, and sample SVG download.

No browser JavaScript errors were observed. Physical device haptic strength and live microphone capture have not been validated on a real phone.
