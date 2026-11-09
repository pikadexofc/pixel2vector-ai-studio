#!/usr/bin/env python3
"""Create a deterministic ZIP for a portable Agent Plugin package."""
from __future__ import annotations
import argparse, hashlib, json, os, stat, sys, tempfile, zipfile
from pathlib import Path
from typing import Any

# Support both `python -m scripts.package_plugin` and direct CLI execution.
_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(_REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPOSITORY_ROOT))

from scripts.validate_plugin import validate_plugin
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".github", ".worktrees", ".superpowers"}
SKIP_FILES = {".gitignore", ".gitattributes", ".editorconfig"}
ARCHIVE_ROOT = "pixelperfect-studio"

def snapshot(root: Path) -> dict[str, tuple[bytes, bool]]:
    entries: dict[str, tuple[bytes, bool]] = {}; folded = set()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts): continue
        if path.is_symlink(): raise ValueError(f"Symlink not packaged: {rel.as_posix()}")
        if not path.is_file() or path.name in SKIP_FILES: continue
        name = rel.as_posix()
        if "\\" in name or name.startswith("/") or ".." in Path(name).parts: raise ValueError(f"Unsafe archive path: {name}")
        key = name.casefold()
        if key in folded: raise ValueError(f"Case-insensitive path collision: {name}")
        folded.add(key); payload = path.read_bytes()
        if len(payload) > 100 * 1024 * 1024: raise ValueError(f"File too large: {name}")
        entries[name] = (payload, bool(path.stat().st_mode & stat.S_IXUSR))
    if not entries: raise ValueError("No package files found")
    return entries

def build_package(plugin_root: Path | str, output_zip: Path | str) -> dict[str, Any]:
    root = Path(plugin_root).expanduser().resolve(strict=True); validation = validate_plugin(root)
    output = Path(output_zip).expanduser().resolve()
    try: output.relative_to(root)
    except ValueError: pass
    else: raise ValueError("Output ZIP must be outside plugin root")
    output.parent.mkdir(parents=True, exist_ok=True); entries = snapshot(root)
    fd, tmp_name = tempfile.mkstemp(prefix=".pixelperfect-", suffix=".zip", dir=output.parent); os.close(fd); tmp = Path(tmp_name)
    try:
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, (payload, executable) in sorted(entries.items()):
                archive_name = f"{ARCHIVE_ROOT}/{name}"
                info = zipfile.ZipInfo(archive_name, date_time=(2020,1,1,0,0,0)); info.compress_type = zipfile.ZIP_DEFLATED; info.create_system = 3
                info.external_attr = (stat.S_IFREG | (0o755 if executable else 0o644)) << 16; info.create_version = 20; info.extract_version = 20
                archive.writestr(info, payload)
        digest = hashlib.sha256(tmp.read_bytes()).hexdigest(); os.replace(tmp, output)
    finally: tmp.unlink(missing_ok=True)
    return {"status":"packaged", "plugin":validation["plugin"], "version":validation["version"], "zip":str(output),
            "sha256":digest, "archive_root":ARCHIVE_ROOT, "files":sorted(f"{ARCHIVE_ROOT}/{name}" for name in entries), "file_count":len(entries), "validation_status":validation["status"]}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("plugin_root",type=Path); parser.add_argument("output_zip",type=Path); args=parser.parse_args()
    try: print(json.dumps(build_package(args.plugin_root,args.output_zip),ensure_ascii=False,indent=2)); return 0
    except Exception as exc: print(json.dumps({"status":"failed","error":str(exc)},indent=2),file=__import__("sys").stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
