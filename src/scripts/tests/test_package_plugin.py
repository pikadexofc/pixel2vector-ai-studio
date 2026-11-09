import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_plugin import ARCHIVE_ROOT, build_package
from scripts.build_local_marketplace import build_local_marketplace

ROOT = Path(__file__).resolve().parents[2]


class PluginPackageTests(unittest.TestCase):
    def test_archive_has_exactly_one_top_level_plugin_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "plugin.zip"
            result = build_package(ROOT, output)
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
                roots = {name.split("/", 1)[0] for name in names if "/" in name}
                self.assertEqual(roots, {ARCHIVE_ROOT})
                self.assertIn(f"{ARCHIVE_ROOT}/plugin.json", names)
                self.assertIn(f"{ARCHIVE_ROOT}/.codex-plugin/plugin.json", names)
                self.assertTrue(all(name.startswith(f"{ARCHIVE_ROOT}/") for name in names))
                self.assertEqual(archive.testzip(), None)
            self.assertEqual(result["archive_root"], ARCHIVE_ROOT)

    def test_local_marketplace_installer_uses_actual_plugin_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "marketplace.zip"
            result = build_local_marketplace(ROOT, output)
            self.assertEqual(result["version"], "1.0.0")
            with zipfile.ZipFile(output) as archive:
                installer = archive.read("Install-PixelPerfectStudio.ps1").decode("utf-8")
                readme = archive.read("README-INSTALL.md").decode("utf-8")
                plugin = json.loads(archive.read(".codex/plugins/pixelperfect-studio/plugin.json"))
                self.assertIn("PixelPerfect Studio 1.0.0 files installed locally.", installer)
                self.assertIn("Install PixelPerfect Studio 1.0.0", readme)
                self.assertEqual(plugin["version"], "1.0.0")
                self.assertEqual(archive.testzip(), None)


if __name__ == "__main__":
    unittest.main()
