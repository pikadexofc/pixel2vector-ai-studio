#!/usr/bin/env python3
"""Dependency-free validator for the portable PixelPerfect Studio Agent Plugin."""
from __future__ import annotations
import argparse, json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from typing import Any

PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")
SENSITIVE = {"credentials.json", "auth.json", "id_rsa", "id_ed25519", "authorized_keys", ".env", ".env.local"}
SKIP = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".github", ".worktrees", ".superpowers"}
SKIP_FILES = {".gitignore", ".gitattributes", ".editorconfig"}


def fail(message: str) -> None:
    raise ValueError(message)


def safe_relative(raw: Any, field: str) -> str:
    if not isinstance(raw, str) or not raw or raw != raw.strip(): fail(f"{field}: non-empty relative path required")
    if "\\" in raw or raw.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", raw): fail(f"{field}: absolute paths and backslashes are forbidden")
    if any(p in {"..", "."} for p in PurePosixPath(raw).parts): fail(f"{field}: dot segments are forbidden")
    return raw[2:] if raw.startswith("./") else raw


def read_frontmatter(path: Path) -> tuple[str, str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"): fail(f"{path}: YAML frontmatter must start at line 1")
    end = text.find("\n---\n", 4)
    if end < 0: fail(f"{path}: closing frontmatter delimiter is missing")
    block, body = text[4:end], text[end + 5:].strip()
    if any(x in block for x in ("!!", "&", "*", "<<:")) or "\t" in block: fail(f"{path}: unsupported YAML tags, anchors, aliases, merge keys or tabs")
    values: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"): continue
        if ":" not in line: fail(f"{path}: malformed frontmatter line {line!r}")
        key, value = line.split(":", 1); key = key.strip(); value = value.strip()
        if key in values: fail(f"{path}: duplicate frontmatter field {key}")
        if key not in {"name", "description", "license", "compatibility"}: fail(f"{path}: unsupported frontmatter field {key}")
        if value.startswith(("!", "&", "*", "{", "[")): fail(f"{path}: unsupported YAML value for {key}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'": value = value[1:-1]
        values[key] = value
    name, description = values.get("name", ""), values.get("description", "")
    if not name or not description or not body: fail(f"{path}: name, description and instruction body are required")
    if len(name) > 64 or not SKILL_NAME.fullmatch(name): fail(f"{path}: invalid Skill name {name!r}")
    if len(description) > 1024 or not description.lower().startswith("use when "): fail(f"{path}: description must start 'Use when ...' and be <=1024 chars")
    if len(values.get("compatibility", "")) > 500: fail(f"{path}: compatibility exceeds 500 chars")
    return name, description, body


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    def luminance(value: str) -> float:
        rgb = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    a, b = sorted((luminance(hex_a), luminance(hex_b)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def validate_svg(path: Path) -> None:
    try: element = ET.parse(path).getroot()
    except ET.ParseError as exc: fail(f"{path}: malformed SVG: {exc}")
    if element.tag.split("}")[-1] != "svg": fail(f"{path}: root element is not svg")
    view = element.attrib.get("viewBox", "").replace(",", " ").split()
    if len(view) != 4: fail(f"{path}: SVG viewBox must have four numeric values")
    try: _, _, w, h = map(float, view)
    except ValueError: fail(f"{path}: SVG viewBox must be numeric")
    if w <= 0 or h <= 0 or abs(w-h) > 1e-6: fail(f"{path}: logo SVG viewBox must be square and positive")
    raw = path.read_text(encoding="utf-8")
    if re.search(r"(?:href|src)\s*=\s*['\"]https?://", raw, re.I) or "<script" in raw.lower(): fail(f"{path}: remote references or scripts are forbidden in logo SVG")


def check_markdown_links(path: Path, root: Path) -> int:
    count = 0; text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")): continue
        target = target.split("#", 1)[0]
        if not target: continue
        target = safe_relative(target, f"Markdown link in {path.relative_to(root)}")
        resolved = (path.parent / target).resolve()
        try: resolved.relative_to(root.resolve())
        except ValueError: fail(f"{path}: Markdown link escapes package: {target}")
        if not resolved.exists(): fail(f"{path}: broken local link: {target}")
        count += 1
    return count


def validate_plugin(plugin_root: Path | str) -> dict[str, Any]:
    root = Path(plugin_root).expanduser().resolve(strict=True)
    if not root.is_dir(): fail("Plugin root must be a directory")
    mp = root / "plugin.json"
    if not mp.is_file(): fail("Portable root plugin.json is missing")
    try: manifest = json.loads(mp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: fail(f"plugin.json invalid JSON: {exc}")
    if not isinstance(manifest, dict): fail("plugin.json must be an object")
    allowed = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
    extra = set(manifest) - allowed
    if extra: fail(f"Unsupported plugin.json fields: {sorted(extra)}")
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json": fail("plugin.json must target Agent Plugins schema 1.0.0")
    name, version, description = manifest.get("name"), manifest.get("version"), manifest.get("description")
    if not isinstance(name, str) or len(name) > 64 or not PLUGIN_NAME.fullmatch(name): fail("Plugin name is invalid")
    if not isinstance(version, str) or not SEMVER.fullmatch(version): fail("Plugin version must be strict semver")
    if not isinstance(description, str) or not description.strip(): fail("Plugin description is required")
    author = manifest.get("author", {})
    if not isinstance(author, dict) or any(not isinstance(v, str) for v in author.values()): fail("author must be an object of string fields")
    ext = manifest.get("extensions", {})
    if not isinstance(ext, dict): fail("extensions must be an object")
    oi = ext.get("com.openai", {})
    if not isinstance(oi, dict): fail("extensions.com.openai must be an object")
    interface = oi.get("interface", {})
    if not isinstance(interface, dict): fail("interface must be an object")
    for field, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000)):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > limit: fail(f"interface.{field} must be non-empty text <= {limit} chars")
        if field != "longDescription" and any(c in value for c in "\r\n"): fail(f"interface.{field} must be one line")
    categories = {"Productivity", "Creativity", "Developer Tools", "Business & Operations", "Data & Analytics", "Communication", "Education & Research", "Security", "Finance", "Healthcare", "Travel", "Entertainment", "Other"}
    if interface.get("category") not in categories: fail("interface.category is not a supported category")
    caps = interface.get("capabilities", [])
    if not isinstance(caps, list) or len(caps) > 20 or any(not isinstance(x, str) or not x.strip() or len(x) > 120 or "\n" in x for x in caps): fail("interface.capabilities must be <=20 concise strings")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or len(prompts) > 3 or any(not isinstance(x, str) or not x.strip() or len(x) > 128 or "\n" in x for x in prompts): fail("interface.defaultPrompt must contain <=3 prompts of <=128 chars")
    if len({" ".join(x.split()).casefold() for x in prompts}) != len(prompts): fail("interface.defaultPrompt has duplicate prompts")
    developer_name = interface.get("developerName")
    if not isinstance(developer_name, str) or not developer_name.strip() or len(developer_name) > 80 or any(c in developer_name for c in "\r\n"):
        fail("interface.developerName must be non-empty, single-line text <=80 chars")
    color = interface.get("brandColor")
    if color is not None:
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color): fail("interface.brandColor must be #RRGGBB")
        if contrast_ratio(color, "#FFFFFF") < 2.0: fail("interface.brandColor must have >=2:1 contrast against white")
    dark_color = interface.get("brandColorDark")
    if dark_color is not None:
        if not isinstance(dark_color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", dark_color): fail("interface.brandColorDark must be #RRGGBB")
        if contrast_ratio(dark_color, "#212121") < 2.0: fail("interface.brandColorDark must have >=2:1 contrast against #212121")
    if interface.get("screenshots"): fail("Skills-only plugin cannot declare screenshots")
    for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if field not in interface:
            if field in {"logo", "composerIcon"}: fail(f"interface.{field} is required")
            continue
        rel = safe_relative(interface.get(field), f"interface.{field}")
        target = (root / rel).resolve()
        try: target.relative_to(root)
        except ValueError: fail(f"interface.{field} escapes the plugin root")
        if not target.is_file(): fail(f"interface.{field} missing file: {rel}")
        if target.stat().st_size > 5 * 1024 * 1024: fail(f"interface.{field} exceeds 5 MiB")
        if target.suffix.lower() not in {".svg", ".png", ".jpg", ".jpeg", ".webp"}: fail(f"interface.{field} has unsupported image format")
        if target.suffix.lower() == ".svg": validate_svg(target)
    onboarding = oi.get("onboardingSkill")
    if onboarding and not (root / safe_relative(onboarding, "onboardingSkill")).is_file(): fail("onboardingSkill points to a missing file")
    skills_root = root / "skills"
    if not skills_root.is_dir(): fail("skills/ is missing")
    skills = []
    for folder in sorted(skills_root.iterdir()):
        if folder.is_symlink() or not folder.is_dir(): fail(f"skills/ must contain only directories, found {folder.name}")
        skill_file = folder / "SKILL.md"
        if not skill_file.is_file(): fail(f"{folder.name} is missing SKILL.md")
        skill_name, skill_desc, _ = read_frontmatter(skill_file)
        if skill_name != folder.name: fail(f"Skill frontmatter name {skill_name!r} does not match directory {folder.name!r}")
        if len(f"{name}:{skill_name}") > 64: fail(f"Combined plugin/skill identity exceeds 64 characters: {skill_name}")
        skills.append({"slug": folder.name, "name": skill_name, "description": skill_desc})
    if not skills: fail("At least one Skill is required")
    if len({s["name"] for s in skills}) != len(skills): fail("Skill names must be unique")
    compat = root / ".codex-plugin" / "plugin.json"
    if compat.exists():
        if not compat.is_file(): fail(".codex-plugin/plugin.json must be a file")
        if [p.name for p in (root / ".codex-plugin").iterdir()] != ["plugin.json"]: fail("Only plugin.json may be stored inside .codex-plugin/")
        cm = json.loads(compat.read_text(encoding="utf-8"))
        if not isinstance(cm, dict) or cm.get("skills", "./skills/") not in {"./skills/", "./skills"}: fail("Compatibility manifest must declare skills: ./skills/")
        if any(k in cm for k in ("mcpServers", "apps")): fail("This package is skills-only; no MCP/app declarations")
    files, links = [], 0
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(p in SKIP for p in rel.parts) or path.name in SKIP_FILES: continue
        if path.is_symlink(): fail(f"Symlink is not allowed: {rel.as_posix()}")
        if not path.is_file(): continue
        relname = rel.as_posix()
        if "\\" in relname or len(relname) > 1024: fail(f"Unsafe or long path: {relname}")
        low = path.name.lower()
        if low in SENSITIVE or low.startswith(".env") or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}: fail(f"Sensitive filename: {relname}")
        if path.suffix.lower() in {".pyc", ".pyo"} or path.name in {".DS_Store", "Thumbs.db"}: fail(f"Generated file should not be packaged: {relname}")
        files.append(relname)
        if path.suffix.lower() in {".md", ".markdown"}: links += check_markdown_links(path, root)
    return {"status":"passed", "plugin":name, "version":version, "skill_count":len(skills), "skills":skills,
            "asset_declarations_checked":sum(1 for field in ("logo", "composerIcon", "logoDark", "composerIconDark") if field in interface), "file_count":len(files), "local_markdown_links_checked":links,
            "architecture":"skills-only", "manifest":"portable-root-plugin-json", "compatibility_manifest":compat.exists(),
            "warnings":["ChatGPT desktop import was not exercised; public listing and publisher approval remain external gates."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("plugin_root", type=Path); parser.add_argument("--json", action="store_true"); args = parser.parse_args()
    try: print(json.dumps(validate_plugin(args.plugin_root), ensure_ascii=False, indent=2)); return 0
    except Exception as exc: print(json.dumps({"status":"failed", "error":str(exc)}, indent=2), file=sys.stderr); return 1

if __name__ == "__main__": raise SystemExit(main())
