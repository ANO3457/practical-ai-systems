import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_web_lockfiles import main as check_web_lockfiles


class WebLockfileTests(unittest.TestCase):
    def test_accepts_matching_lockfile(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            web = root / "systems" / "demo" / "web"
            web.mkdir(parents=True)
            (web / "package.json").write_text(json.dumps({"devDependencies": {"typescript": "5.6.3"}}))
            (web / "package-lock.json").write_text(json.dumps({
                "lockfileVersion": 3,
                "packages": {"": {"devDependencies": {"typescript": "5.6.3"}}},
            }))
            self.assertEqual(check_web_lockfiles(root), 0)

    def test_rejects_missing_lockfile(self):
        with tempfile.TemporaryDirectory() as temp:
            web = Path(temp) / "systems" / "demo" / "web"
            web.mkdir(parents=True)
            (web / "package.json").write_text("{}")
            self.assertEqual(check_web_lockfiles(Path(temp)), 1)

    def test_rejects_mismatched_dependencies(self):
        with tempfile.TemporaryDirectory() as temp:
            web = Path(temp) / "systems" / "demo" / "web"
            web.mkdir(parents=True)
            (web / "package.json").write_text(json.dumps({"devDependencies": {"typescript": "5.6.3"}}))
            (web / "package-lock.json").write_text(json.dumps({
                "lockfileVersion": 3,
                "packages": {"": {"devDependencies": {"typescript": "5.7.0"}}},
            }))
            self.assertEqual(check_web_lockfiles(Path(temp)), 1)


if __name__ == "__main__":
    unittest.main()
