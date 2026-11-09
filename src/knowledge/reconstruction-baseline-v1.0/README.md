# PixelPerfect Studio Learning Archive v1.0

**Record date:** 2026-11-03  
**Purpose:** Preserve the learning, defects, corrections, evidence and proposed operating rules from three reconstruction exercises before changing the plugin implementation.

## Contents

- `LEARNINGS-AND-FIXES.md`: consolidated findings across all three projects.
- `OPERATING-RULES.md`: proposed mandatory reconstruction and QA rules.
- `DEFECT-AND-CORRECTION-REGISTER.md`: defect log with evidence and fix status.
- `STRUCTURED-LEARNING.json`: machine-readable knowledge records for later plugin integration.
- `EVIDENCE-REGISTER.json`: file inventory, key values and confidence classification.
- `evidence/`: copies of the source workflow record and project analysis, manifests, QA reports, asset registers and stage ledgers.

## Evidence policy

This archive distinguishes:

- **ARTIFACT_VERIFIED**: directly present in a supplied or generated project artifact that was inspected for this archive.
- **SOURCE_RECORDED**: stated in the uploaded executed-workflow JSON, but not independently rerun here.
- **CONVERSATION_REPORTED**: a correction or observation reported during the interactive build, without a retained machine-readable proof for that specific change.
- **INFERENCE**: a recommended engineering rule derived from the evidence.
- **OPEN**: unresolved or not yet verified.

A stage marked complete does not mean visual fidelity passed. Rendering success, structural validity and similarity are separate gates.

## Scope and change control

This is a learning and documentation archive only. It does **not** modify the PixelPerfect Studio plugin ZIP, plugin skills, schemas, or production code. Plugin integration should happen only after review of this archive.
