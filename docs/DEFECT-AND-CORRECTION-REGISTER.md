# Defect and Correction Register

| ID | Project | Defect / risk | Evidence | Status | Required durable fix |
|---|---|---|---|---|---|
| PP-D001 | SubPilot | Headline overflow in early render | Build discussion; final QA verifies containment | Corrected locally | Add text-box boundary assertion and font-metric capture |
| PP-D002 | SubPilot | Player face read incorrectly | Build discussion; final QA says paths reconstructed | Corrected locally, source-trace still open | Trace from source or document generated vector shape and inspect at native size |
| PP-D003 | SubPilot | Lower section and wordmark placement off | Coordinate review during build | Revised locally | Manifest geometry checks against source landmarks |
| PP-D004 | SubPilot | Exact fonts unknown | `analysis.json`, `qa-report.json` | Open | Font search then raster glyph extraction/SVG fallback |
| PP-D005 | SubPilot | Grain and halftone approximated | `analysis.json`, `qa-report.json` | Open | Source texture extraction and separate texture masks |
| PP-D006 | SubPilot | QR destination unverified | `asset-register.json`, `qa-report.json` | Open | Decode and verify payload before replacing or certifying |
| PP-D007 | After the Noise | Shared CSS positioning rule overrode headline placement | Build iteration notes | Corrected locally | Scoped CSS and computed-bounds regression test |
| PP-D008 | After the Noise | Layer stack order wrong | Build iteration notes | Corrected locally | Explicit z-index bands plus overlap assertions |
| PP-D009 | After the Noise | Paper tears/right concrete upright missing or too clean | Asset register has nine source-extracted cutouts | Corrected in build | Mask edge QA, halos/gaps inspection and local difference review |
| PP-D010 | After the Noise | Approximate headline font | `analysis.json`, `qa-report.json` | Open | Exact-font search, then glyph extraction |
| PP-D011 | After the Noise | Regional mismatch remains | QA report: 16.72% mismatch, MAE 24.8132, SSIM 0.7281 | Open | Targeted corrections to typography, texture and masks; rerun metrics |
| PP-D012 | After the Noise | README lists 14 layers, manifest has 16 | README vs `layer-manifest.json` and `stage-ledger.json` | Confirmed documentation defect | Generate count from manifest and validate all counts |
| PP-D013 | After the Noise | Filename extension `.png`, actual format JPEG | `analysis.json`, source metadata | Detected and documented | Detect format from bytes; store supplied filename and detected format separately |
| PP-D014 | Legal cover workflow | No numerical visual similarity score | Uploaded workflow JSON, phase 7 limitations | Known QA gap | Add difference map, mismatch ratio, MAE and SSIM with parameters |
| PP-D015 | Legal cover workflow | Workflow record's 35-layer equality is recorded but not independently rerun in this archive | Uploaded workflow JSON, phase 8 | Source-recorded only | Retain machine-check output or rerun the validator on final files |
| PP-D016 | All | Render success can be confused with fidelity acceptance | All three project QA records | Product-level risk | Adopt staged status vocabulary and reject pixel-perfect claims without evidence |
| PP-D017 | All | Extraction/generation decision can be inconsistent | Legal workflow vs poster tests | Improvement required | Use source extraction first for reference-embedded elements; generation only when extraction fails quality gates |
| PP-D018 | All | Manifest and output metadata may drift | 14 vs 16 layer discrepancy | Open | Add a release validator for IDs, counts, asset hashes and output dimensions |

## Status definitions

- **Corrected locally / in build:** the project iteration contains a correction; the plugin itself has not yet been updated with a permanent automated rule.
- **Open:** still listed as a known limitation or requires a new test.
- **Source-recorded only:** asserted by the uploaded workflow record, not independently reproduced during this documentation pass.
