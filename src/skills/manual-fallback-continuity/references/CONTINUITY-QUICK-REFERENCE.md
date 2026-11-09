# Continuity Quick Reference

## Required behavior

When an integrated service fails and the current ChatGPT conversation remains available, continue the same customer job manually using accessible references and host tools. Preserve completed work, explain only the unavailable capabilities, and create an internal portable checkpoint. Do not expose it or any related project artefact as a reconstruction deliverable. Never claim a cloud action or measurement that did not happen.

## Architecture contract

The full service-by-service matrix and twelve acceptance scenarios live at `docs/architecture/MANUAL-CONTINUITY-CONTRACT.md`.

## Checkpoint contract

Use `schemas/continuity-checkpoint.schema.json` and `examples/continuity-checkpoint.example.json`. A checkpoint records project identity, current stage, stage ledger, source availability, artifacts, fallback reason, limitations, open items, and one next action. It must not contain credentials, signed URLs, or binary contents.

## Handoff generator

Run `python3 scripts/build_chatgpt_handoff.py path/to/checkpoint.json --out path/to/manual-handoff.md` to create an internal ready-to-paste ChatGPT continuation brief. Never attach or link it as part of a reconstruction handoff. The generator rejects checkpoints that do not explicitly confirm that credentials are absent and that the checkpoint is safe to share.
