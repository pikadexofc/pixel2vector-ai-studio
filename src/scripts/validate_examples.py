#!/usr/bin/env python3
"""Validate bundled JSON examples and plugin manifest against packaged schemas."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("Missing optional dependency: install jsonschema with `python3 -m pip install 'jsonschema>=4.20,<5'`.", file=sys.stderr)
    raise SystemExit(2)

EXAMPLES = {
    "reference-analysis.example.json": "visual-analysis.schema.json",
    "layer-manifest.example.json": "layer-manifest.schema.json",
    "asset-record.example.json": "asset-record.schema.json",
    "qa-report.example.json": "qa-report.schema.json",
    "standalone-html-delivery.example.json": "standalone-html-delivery.schema.json",
    "evidence-record.example.json": "evidence-record.schema.json",
    "figma-mapping.example.json": "figma-mapping.schema.json",
    "continuity-checkpoint.example.json": "continuity-checkpoint.schema.json",
}


def validate(root: Path) -> dict:
    schema_dir = root / "schemas"
    example_dir = root / "examples"
    results = []
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    manifest_schema = json.loads((schema_dir / "agent-plugin-1.0.0.schema.json").read_text(encoding="utf-8"))
    cases = [("plugin.json", manifest, manifest_schema)]
    for example_name, schema_name in EXAMPLES.items():
        instance = json.loads((example_dir / example_name).read_text(encoding="utf-8"))
        schema = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
        cases.append((example_name, instance, schema))
    for name, instance, schema in cases:
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(map(str, error.absolute_path)))
        results.append({"file": name, "status": "passed" if not errors else "failed", "errors": [
            {"path": "/".join(map(str, error.absolute_path)), "message": error.message} for error in errors
        ]})
    return {"status": "passed" if all(item["status"] == "passed" for item in results) else "failed", "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = validate(args.plugin_root.resolve(strict=True))
    except Exception as error:
        print(json.dumps({"status": "failed", "error": str(error)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
