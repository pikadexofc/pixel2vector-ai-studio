import os
import unittest
import json

class TestPixel2Vector(unittest.TestCase):
    def setUp(self):
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_manifest_and_icons(self):
        icon_path = os.path.join(self.root, "assets", "icons", "icon-128.png")
        self.assertTrue(os.path.exists(icon_path), "Primary 128px icon must exist")

    def test_gui_exists(self):
        index_path = os.path.join(self.root, "index.html")
        self.assertTrue(os.path.exists(index_path), "index.html GUI must exist")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Pixel2Vector AI Studio", content)

    def test_plugin_manifest(self):
        plugin_path = os.path.join(self.root, "src", "plugin.json")
        if os.path.exists(plugin_path):
            with open(plugin_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("name", data)

    def test_cubic_bezier_math(self):
        # Parametric cubic bezier: B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1 + 3(1-t)t^2 P2 + t^3 P3
        p0, p1, p2, p3 = 0.0, 0.5, 0.8, 1.0
        t = 0.5
        val = (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t)*(t**2) * p2 + (t**3) * p3
        self.assertAlmostEqual(val, 0.5875, places=4)

if __name__ == "__main__":
    unittest.main()
