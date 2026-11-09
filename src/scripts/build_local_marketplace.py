#!/usr/bin/env python3
"""Build a deterministic Windows-friendly personal marketplace installer ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
import zipfile
from pathlib import Path
from typing import Any

PLUGIN_SLUG = "pixelperfect-studio"
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "tests", ".worktrees"}
SKIP_NAMES = {".DS_Store", ".gitignore", ".gitattributes", ".editorconfig"}


def _marketplace_manifest() -> bytes:
    manifest = {
        "name": "pickko-personal-plugins",
        "interface": {"displayName": "Pickko Personal Plugins"},
        "plugins": [
            {
                "name": PLUGIN_SLUG,
                "source": {
                    "source": "local",
                    "path": "./.codex/plugins/pixelperfect-studio",
                },
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Creativity",
            }
        ],
    }
    return (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _installer_script(version: str) -> bytes:
    script = r'''$ErrorActionPreference = "Stop"
$PluginSlug = "pixelperfect-studio"
$SourcePlugin = Join-Path $PSScriptRoot ".codex\plugins\pixelperfect-studio"
$HomeRoot = $HOME
$TargetPlugin = Join-Path $HomeRoot ".codex\plugins\pixelperfect-studio"
$MarketplaceDir = Join-Path $HomeRoot ".agents\plugins"
$MarketplaceFile = Join-Path $MarketplaceDir "marketplace.json"
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

if (-not (Test-Path -LiteralPath (Join-Path $SourcePlugin "plugin.json"))) {
    throw "The bundled PixelPerfect Studio plugin folder is missing or incomplete. Extract the full ZIP before running this script."
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $TargetPlugin) | Out-Null
$BackupPlugin = $null
if (Test-Path -LiteralPath $TargetPlugin) {
    $BackupPlugin = "$TargetPlugin.backup-$Timestamp"
    Move-Item -LiteralPath $TargetPlugin -Destination $BackupPlugin
    Write-Host "Existing plugin backed up to: $BackupPlugin"
}
try {
    Copy-Item -LiteralPath $SourcePlugin -Destination $TargetPlugin -Recurse -Force
} catch {
    if ($BackupPlugin -and (Test-Path -LiteralPath $BackupPlugin) -and -not (Test-Path -LiteralPath $TargetPlugin)) {
        Move-Item -LiteralPath $BackupPlugin -Destination $TargetPlugin
    }
    throw
}

New-Item -ItemType Directory -Force -Path $MarketplaceDir | Out-Null
if (Test-Path -LiteralPath $MarketplaceFile) {
    Copy-Item -LiteralPath $MarketplaceFile -Destination "$MarketplaceFile.backup-$Timestamp"
    $Marketplace = Get-Content -LiteralPath $MarketplaceFile -Raw | ConvertFrom-Json
    if (-not $Marketplace.name) { $Marketplace | Add-Member -NotePropertyName name -NotePropertyValue "pickko-personal-plugins" }
    if (-not $Marketplace.interface) {
        $Marketplace | Add-Member -NotePropertyName interface -NotePropertyValue ([PSCustomObject]@{ displayName = "Pickko Personal Plugins" })
    }
    $ExistingPlugins = @()
    if ($Marketplace.plugins) { $ExistingPlugins = @($Marketplace.plugins) }
    $Marketplace.plugins = @($ExistingPlugins | Where-Object { $_.name -ne $PluginSlug })
} else {
    $Marketplace = [PSCustomObject]@{
        name = "pickko-personal-plugins"
        interface = [PSCustomObject]@{ displayName = "Pickko Personal Plugins" }
        plugins = @()
    }
}

$PluginEntry = [PSCustomObject]@{
    name = $PluginSlug
    source = [PSCustomObject]@{
        source = "local"
        path = "./.codex/plugins/pixelperfect-studio"
    }
    policy = [PSCustomObject]@{
        installation = "AVAILABLE"
        authentication = "ON_INSTALL"
    }
    category = "Creativity"
}
$Marketplace.plugins = @($Marketplace.plugins) + @($PluginEntry)
$Marketplace | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $MarketplaceFile -Encoding UTF8

Write-Host "PixelPerfect Studio {version} files installed locally."
Write-Host "Plugin folder: $TargetPlugin"
Write-Host "Marketplace:   $MarketplaceFile"
Write-Host "Next: restart the ChatGPT desktop app, open Plugins > Personal, and install PixelPerfect Studio."
'''
    return script.encode("utf-8").replace(b"{version}", version.encode("utf-8"))


def build_local_marketplace(plugin_root: Path | str, output_zip: Path | str) -> dict[str, Any]:
    root = Path(plugin_root).expanduser().resolve(strict=True)
    plugin_manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    if plugin_manifest.get("name") != PLUGIN_SLUG:
        raise ValueError(f"Expected plugin name {PLUGIN_SLUG!r}")
    version = plugin_manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("Plugin version is missing")

    output = Path(output_zip).expanduser().resolve()
    if output.is_relative_to(root):
        raise ValueError("Output ZIP must be outside the plugin root")

    entries: dict[str, tuple[bytes, bool]] = {
        (".agents/plugins/marketplace.json"): (_marketplace_manifest(), False),
        ("Install-PixelPerfectStudio.ps1"): (_installer_script(version), False),
        ("README-INSTALL.md"): (f"""# Install PixelPerfect Studio {version} on Windows\n\n1. Extract this ZIP to a permanent folder.\n2. Open PowerShell in the extracted folder.\n3. Run `powershell -ExecutionPolicy Bypass -File .\\Install-PixelPerfectStudio.ps1`.\n4. Restart the ChatGPT desktop app.\n5. Open Plugins, choose your Personal marketplace, install PixelPerfect Studio, and start a new conversation.\n\nThe installer backs up an existing PixelPerfect folder and preserves all other entries in your personal marketplace. It does not publish the plugin or connect external services. Local marketplace installation is supported through the ChatGPT desktop app; this package cannot install itself into a remote or mobile ChatGPT session.\n""".encode("utf-8"), False),
    }

    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_PARTS for part in rel.parts) or path.name in SKIP_NAMES:
            continue
        if path.is_symlink():
            raise ValueError(f"Symlink not packaged: {rel.as_posix()}")
        if not path.is_file():
            continue
        rel_name = rel.as_posix()
        if "\\" in rel_name or ".." in Path(rel_name).parts:
            raise ValueError(f"Unsafe plugin path: {rel_name}")
        archive_name = f".codex/plugins/{PLUGIN_SLUG}/{rel_name}"
        if archive_name.casefold() in {name.casefold() for name in entries}:
            raise ValueError(f"Duplicate archive path: {archive_name}")
        info = path.stat()
        entries[archive_name] = (path.read_bytes(), bool(info.st_mode & stat.S_IXUSR))

    output.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".pixelperfect-marketplace-", suffix=".zip", dir=output.parent)
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, (payload, executable) in sorted(entries.items()):
                info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | (0o755 if executable else 0o644)) << 16
                info.create_version = 20
                info.extract_version = 20
                archive.writestr(info, payload)
        digest = hashlib.sha256(tmp.read_bytes()).hexdigest()
        os.replace(tmp, output)
    finally:
        tmp.unlink(missing_ok=True)

    return {
        "status": "packaged",
        "plugin": PLUGIN_SLUG,
        "version": version,
        "zip": str(output),
        "sha256": digest,
        "file_count": len(entries),
        "marketplace": ".agents/plugins/marketplace.json",
        "install_script": "Install-PixelPerfectStudio.ps1",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_root", type=Path)
    parser.add_argument("output_zip", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(build_local_marketplace(args.plugin_root, args.output_zip), indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
