import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_web_lockfiles import main


class InvalidLockShapes(unittest.TestCase):
    def check_pair(self, package, lock):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            web = root / 'systems/demo/web'
            web.mkdir(parents=True)
            (web / 'package.json').write_text(json.dumps(package), encoding='utf-8')
            (web / 'package-lock.json').write_text(json.dumps(lock), encoding='utf-8')
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                result = main(root)
            self.assertEqual(result, 1)
            self.assertIn('systems', stderr.getvalue())
            self.assertIn('demo', stderr.getvalue())

    def test_wrong_json_containers_are_diagnostics(self):
        good = {'lockfileVersion': 3, 'packages': {'': {}}}
        for package, lock in [([], good), ({}, []), ({}, {'lockfileVersion': 3, 'packages': []}), ({}, {'lockfileVersion': 3, 'packages': {'': []}})]:
            with self.subTest(package=package, lock=lock):
                self.check_pair(package, lock)

    def test_invalid_versions_are_diagnostics(self):
        for version in ['3', None, True, 2.5]:
            with self.subTest(version=version):
                self.check_pair({}, {'lockfileVersion': version, 'packages': {'': {}}})

    def test_dependency_sections_must_be_objects_even_when_equal(self):
        for section in ['dependencies', 'devDependencies', 'optionalDependencies']:
            for value in [[], None, 'typescript']:
                with self.subTest(section=section, value=value):
                    self.check_pair({section: value}, {'lockfileVersion': 3, 'packages': {'': {section: value}}})
