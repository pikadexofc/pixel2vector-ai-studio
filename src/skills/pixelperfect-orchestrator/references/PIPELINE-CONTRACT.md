# Pipeline contracts

| State | Required inputs | Required outputs | Exit gate |
|---|---|---|---|
| INTAKE | user request, source refs | project brief, constraints, availability map | objective and target output unambiguous |
| FORENSICS | immutable source, normalizer | visual-analysis JSON, evidence map | measurements, confidence and unknowns present |
| LAYER_PLAN | analysis JSON | versioned layer manifest | all significant visible elements represented |
| ASSET_PLAN | manifest | per-layer method, source/generation decisions | rights and method decisions recorded |
| ASSET_READY | selected assets | immutable asset versions and metadata | bytes inspected, hash recorded, licence eligible |
| COMPILE | frozen manifest/assets | standalone HTML candidate and internal compile metadata | HTML is self-contained; all layers/assets resolve |
| RENDER | compilation | exact-size render and environment record | canvas equals target dimensions |
| QA | reference and render | internal QA evidence, metrics, region checks and defect list | all three passes, calibrated thresholds and release hash pass |
| CORRECT | defect list | targeted patch and new render | defect verification complete |
| LEARN | all project artifacts | learning event, candidate knowledge records | evidence and trust status recorded |
| DELIVER | verified HTML and passing internal evidence | one standalone `.html` file only | `DELIVERABLE_VERIFIED`; no companion artifacts are exposed |

## Recovery

A failed stage retains its inputs and partial outputs with status `FAILED` or `BLOCKED`. Activate `manual-fallback-continuity` and continue the same job in ChatGPT whenever the current conversation and relevant host capabilities remain available. Re-run only after the failure cause is classified. Use idempotency keys for side-effecting stages. If upstream inputs change, mark downstream artefacts stale rather than reusing them silently. Create/update a portable continuity checkpoint whenever a stage is blocked or execution mode changes.

## Parallelism

Allowed when tasks consume immutable inputs and write to separate output namespaces. For example, typography analysis and colour sampling can run in parallel after normalization. Compilation cannot begin until both analysis and asset approvals are frozen. QA cannot begin until the render exists.

## Retry policy

Retry transient network or service errors only when the operation is safe and idempotent. Do not retry permission errors, invalid input, rights uncertainty, or destructive writes without a corrected request. Bound attempts and record each attempt.


## Customer delivery gate

`DELIVER` runs only after `scripts/validate_standalone_delivery.py` passes against the exact HTML, frozen manifest, QA evidence, original reference image and final render capture. The validator recomputes RGB max-channel mismatch ratio, RGB MAE and SSIM, verifies actual image hashes and dimensions, checks exact manifest/HTML ID equality, enforces embedded resources, and compares metrics with a validated acceptance profile. Any post-QA HTML edit invalidates the recorded hash and requires a full rerun.
