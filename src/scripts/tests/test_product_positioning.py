import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ProductPositioningTests(unittest.TestCase):
    def setUp(self):
        self.portable = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.compat = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.interface = self.portable["extensions"]["com.openai"]["interface"]

    def test_manifest_versions_are_aligned_at_production_release(self):
        self.assertEqual(self.portable["version"], "1.0.0")
        self.assertEqual(self.compat["version"], self.portable["version"])

    def test_product_description_identifies_image_to_layered_html(self):
        description = self.portable["description"].casefold()
        self.assertIn("flat image", description)
        self.assertIn("editable", description)
        self.assertIn("fixed-size", description)
        self.assertIn("not a responsive website", description)

    def test_listing_description_explains_separate_components_and_png_assets(self):
        description = self.interface["longDescription"].casefold()
        self.assertIn("separates its meaningful components", description)
        self.assertIn("individual png assets", description)
        self.assertIn("static design canvas", description)
        self.assertIn("standalone html file only", description)

    def test_short_description_and_prompts_fit_host_limits(self):
        self.assertLessEqual(len(self.interface["shortDescription"]), 30)
        self.assertLessEqual(len(self.interface["longDescription"]), 4000)
        self.assertLessEqual(len(self.interface["defaultPrompt"]), 3)
        self.assertTrue(all(len(prompt) <= 128 for prompt in self.interface["defaultPrompt"]))
        self.assertIn("layered html", self.interface["defaultPrompt"][0].casefold())

    def test_onboarding_defaults_to_image_reconstruction_not_website_build(self):
        setup = (ROOT / "skills/setup/SKILL.md").read_text(encoding="utf-8").casefold()
        self.assertIn("editable html design", setup)
        self.assertIn("not a responsive website", setup)
        self.assertIn("do not silently convert it into a responsive website", setup)

    def test_asset_skill_requires_separate_png_generation_and_inspection(self):
        asset = (ROOT / "skills/asset-intelligence/SKILL.md").read_text(encoding="utf-8").casefold()
        self.assertIn("generate each independent visual subject", asset)
        self.assertIn("separate png", asset)
        self.assertIn("inspect the actual returned image", asset)
        self.assertIn("embed it independently", asset)

    def test_compiler_preserves_independent_layers_instead_of_flattening(self):
        compiler = (ROOT / "skills/deterministic-reconstruction/SKILL.md").read_text(encoding="utf-8").casefold()
        self.assertIn("not a website", compiler)
        self.assertIn("own dom element", compiler)
        self.assertIn("not be baked together into a composite", compiler)

    def test_customer_handoff_is_one_html_file_only(self):
        contract = (ROOT / "resources/FINAL-HTML-ONLY-DELIVERY.md").read_text(encoding="utf-8").casefold()
        self.assertIn("one deliverable", contract)
        self.assertIn("separate photographic or illustrative assets remain separate image elements", contract)
        self.assertIn("do not attach or link previews", contract)


if __name__ == "__main__":
    unittest.main()
