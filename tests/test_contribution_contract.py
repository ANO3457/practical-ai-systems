import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.check_systems import check_all, check_system
from scripts.new_system import scaffold
from scripts.registry import load_manifests

ROOT = Path(__file__).resolve().parents[1]


class ContributionContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "systems").mkdir()
        shutil.copytree(ROOT / "templates", self.tmp / "templates")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _scaffold(self, name="demo_sys"):
        return scaffold(name, "Demo", "Beginner", "Classify length.", "None.", root=self.tmp)

    def test_repository_systems_pass_contract(self):
        self.assertEqual(check_all(), [])

    def test_scaffold_creates_manifest_discovered_by_registry(self):
        self._scaffold()
        manifests = load_manifests(self.tmp)
        self.assertIn("demo_sys", manifests)
        self.assertEqual(manifests["demo_sys"]["order"], 1)

    def test_fresh_scaffold_is_flagged_until_placeholders_are_replaced(self):
        folder = self._scaffold()
        errors = check_system(folder)
        self.assertTrue(any("placeholder" in e for e in errors))

    def test_scaffold_rejects_bad_names_and_duplicates(self):
        with self.assertRaises(ValueError):
            scaffold("Bad-Name", "x", "Beginner", "h", "p", root=self.tmp)
        self._scaffold()
        with self.assertRaises(ValueError):
            self._scaffold()

    def test_cross_system_import_is_rejected(self):
        folder = self._scaffold()
        (folder / "app.py").write_text("from systems.doc_qa.app import DocQA\n")
        self.assertTrue(any("standalone" in e for e in check_system(folder)))

    def test_third_party_import_is_rejected(self):
        folder = self._scaffold()
        (folder / "app.py").write_text("import requests\n")
        self.assertTrue(any("third-party" in e for e in check_system(folder)))

    def test_web_runtime_dependency_is_rejected(self):
        folder = self._scaffold()
        pkg = folder / "web" / "package.json"
        data = json.loads(pkg.read_text())
        data["dependencies"] = {"react": "^18"}
        pkg.write_text(json.dumps(data))
        self.assertTrue(any("zero-dependency" in e for e in check_system(folder)))

    def test_invalid_level_in_manifest_is_rejected(self):
        folder = self._scaffold()
        manifest = folder / "system.json"
        data = json.loads(manifest.read_text())
        data["level"] = "Expert"
        manifest.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            load_manifests(self.tmp)


if __name__ == "__main__":
    unittest.main()
