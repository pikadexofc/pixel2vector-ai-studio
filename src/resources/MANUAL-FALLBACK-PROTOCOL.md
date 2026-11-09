# Manual ChatGPT Fallback Protocol

Use `skills/manual-fallback-continuity/SKILL.md` when any integration or execution service fails. The product rule is simple: user task completion comes first; usage metering is best-effort. Do not stop, delay, or truncate the design job because a usage counter, entitlement lookup, reminder, analytics call, or integrated service failed. Continue in the current ChatGPT conversation with available references and host tools, preserve approved outputs, mark what cannot be verified, and create a resumable checkpoint.

The full component matrix and acceptance tests are in `docs/architecture/MANUAL-CONTINUITY-CONTRACT.md`. The portable checkpoint schema and example are `schemas/continuity-checkpoint.schema.json` and `examples/continuity-checkpoint.example.json`.

ChatGPT manual mode cannot execute an unavailable cloud action or guarantee the same speed/measurements as the automated path. It must never fake a render, metric, OCR result, mask, database write, upload, or remote deployment. If ChatGPT itself is unavailable, retain local internal files and the checkpoint for later resumption. Do not expose recovery files as reconstruction deliverables.


## Metering and reminder rule

Deliver the answer first. Reconcile usage and entitlement events after delivery. A usage write failure becomes a pending reconciliation event, not a customer-facing failure. The current Pickko baseline is 100 free completed cycles; reaching the threshold does not cut off a request already in progress. Show a reminder only after delivery and at most once every 20 minutes. Skip reminders when state cannot be verified.


## Reconstruction delivery boundary

For visual reconstruction jobs, fallback changes execution method but never the delivery contract. Keep source code, HTML candidates, manifests, assets, previews, crops, QA evidence and continuity checkpoints internal. Deliver exactly one standalone HTML file only after `DELIVERABLE_VERIFIED`. If the renderer or required verification is unavailable, deliver no file and state the blocker.
