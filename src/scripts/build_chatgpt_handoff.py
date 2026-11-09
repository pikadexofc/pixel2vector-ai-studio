#!/usr/bin/env python3
"""Build a portable, ready-to-paste ChatGPT continuation brief from a checkpoint."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED = {
    "schema_version", "checkpoint_id", "project", "current_stage", "completion_status",
    "user_goal", "source_inputs", "stage_ledger", "artifacts", "fallback", "open_items",
    "next_action", "security_review",
}


def _text(value: Any, fallback: str = "Not recorded") -> str:
    if value is None:
        return fallback
    if isinstance(value, str):
        return value.strip() or fallback
    return str(value)


def validate_checkpoint(checkpoint: dict[str, Any]) -> None:
    if not isinstance(checkpoint, dict):
        raise ValueError("Checkpoint root must be a JSON object")
    missing = sorted(REQUIRED - checkpoint.keys())
    if missing:
        raise ValueError(f"Checkpoint is missing required fields: {', '.join(missing)}")
    security = checkpoint.get("security_review")
    if not isinstance(security, dict):
        raise ValueError("security_review must be an object")
    if security.get("contains_credentials") is not False:
        raise ValueError("Checkpoint must explicitly confirm it contains no credentials")
    if security.get("safe_to_share") is not True:
        raise ValueError("Checkpoint must be reviewed and marked safe_to_share before generating a handoff")
    if not isinstance(checkpoint.get("stage_ledger"), list):
        raise ValueError("stage_ledger must be an array")
    if not isinstance(checkpoint.get("source_inputs"), list):
        raise ValueError("source_inputs must be an array")
    if not isinstance(checkpoint.get("artifacts"), list):
        raise ValueError("artifacts must be an array")


def build_handoff(checkpoint: dict[str, Any]) -> str:
    validate_checkpoint(checkpoint)
    project = checkpoint["project"]
    fallback = checkpoint["fallback"]
    lines = [
        "# Continue manually in ChatGPT",
        "",
        "You are continuing an existing PixelPerfect Studio visual reconstruction job because one or more integrated services are unavailable.",
        "Do not restart the project, ask me to repeat known requirements, or ask me to re-upload a file that is still accessible in this conversation.",
        "Use the reference files already attached to this conversation and the checkpoint details below. If this is a new conversation and an input is marked `requires_reupload`, ask only for that specific missing file.",
        "",
        "## Project",
        f"- Name: {_text(project.get('name'))}",
        f"- Project ID: {_text(project.get('project_id'))}",
        f"- Checkpoint ID: {_text(checkpoint.get('checkpoint_id'))}",
        f"- Canvas: {project.get('canvas', {}).get('width', 'unknown')} × {project.get('canvas', {}).get('height', 'unknown')} px" if isinstance(project.get('canvas'), dict) else "- Canvas: Not recorded",
        f"- Current stage: `{_text(checkpoint.get('current_stage'))}`",
        f"- Completion status: `{_text(checkpoint.get('completion_status'))}`",
        f"- User goal: {_text(checkpoint.get('user_goal'))}",
        "",
        "## Source inputs",
    ]
    if checkpoint["source_inputs"]:
        for item in checkpoint["source_inputs"]:
            lines.append(
                f"- `{_text(item.get('input_id'))}` ({_text(item.get('kind')).replace('_', ' ')}): "
                f"{_text(item.get('description'))}. Availability: `{_text(item.get('availability'))}`."
            )
            if item.get("availability") == "requires_reupload" and item.get("reupload_note"):
                lines.append(f"  - Re-upload only this input: {_text(item.get('reupload_note'))}")
    else:
        lines.append("- No source inputs were recorded. Ask only for the specific missing reference needed to continue.")

    lines.extend(["", "## Completed and pending stages"])
    for stage in checkpoint["stage_ledger"]:
        summary = _text(stage.get("summary"))
        status = _text(stage.get("status"))
        line = f"- `{_text(stage.get('stage'))}`: **{status}**. {summary}"
        if stage.get("failure_reason"):
            line += f" Failure: {_text(stage.get('failure_reason'))}."
        lines.append(line)

    lines.extend(["", "## Existing artifacts"])
    if checkpoint["artifacts"]:
        for artifact in checkpoint["artifacts"]:
            item = (
                f"- `{_text(artifact.get('name'))}` ({_text(artifact.get('kind'))}), "
                f"availability: `{_text(artifact.get('availability'))}`"
            )
            if artifact.get("sha256"):
                item += f", SHA-256: `{artifact['sha256']}`"
            if artifact.get("notes"):
                item += f". {_text(artifact.get('notes'))}"
            lines.append(item)
    else:
        lines.append("- No completed artifacts were recorded.")

    lines.extend([
        "", "## Service failure and fallback",
        f"- Mode: `{_text(fallback.get('mode'))}`",
        f"- Reason: {_text(fallback.get('reason'))}",
        f"- Unavailable services: {', '.join(fallback.get('services_unavailable', [])) or 'None recorded'}",
        "- Limitations: " + ("; ".join(fallback.get("limitations", [])) or "None recorded"),
        "", "## Open items"
    ])
    lines.extend([f"- {item}" for item in checkpoint["open_items"]] or ["- None recorded."])
    lines.extend([
        "", "## Next action", _text(checkpoint.get("next_action")),
        "", "## Instructions for this continuation",
        "1. Continue the same job from the current stage and preserve all approved decisions and artifacts.",
        "2. Use available ChatGPT vision, reasoning, file, Python, code, and artifact tools. Do not assume any external integration is available.",
        "3. Produce the same requested deliverables wherever the current host can genuinely create them.",
        "4. Never claim an upload, OCR run, segmentation, render, numerical metric, database write, cloud job, or Figma operation happened unless it actually did.",
        "5. If rendering or numerical QA cannot run, deliver the editable source and mark those checks pending. Separate manual observations from measured results.",
        "6. Continue through the remaining stages where possible. Do not stop at an error message or ask me to restart.",
        "7. At the end, provide the completed work, residual limitations, and an updated continuity checkpoint with one next action.",
        "", "This handoff contains checkpoint metadata only. Original images, fonts, and other source binaries must remain attached or be re-uploaded only when actually unavailable.",
    ])
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path, help="Path to a continuity checkpoint JSON file")
    parser.add_argument("--out", type=Path, help="Optional output Markdown path; otherwise write to stdout")
    args = parser.parse_args()
    try:
        checkpoint = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        handoff = build_handoff(checkpoint)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(handoff, encoding="utf-8")
        else:
            sys.stdout.write(handoff)
        return 0
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"handoff generation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
