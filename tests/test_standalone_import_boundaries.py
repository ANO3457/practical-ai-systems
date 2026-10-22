import tempfile
import unittest
from pathlib import Path

from scripts.check_systems import check_system


class StandaloneImportBoundaries(unittest.TestCase):
    def import_errors(self, source, nested=False):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / 'systems' / 'demo'
            destination = folder / 'sub' if nested else folder
            destination.mkdir(parents=True)
            (destination / 'app.py').write_text(source, encoding='utf-8')
            return [e for e in check_system(folder) if 'imports ' in e]

    def test_relative_sibling_system_is_refused(self):
        for source in ['from ..other.app import run', 'from .. import other']:
            with self.subTest(source=source):
                self.assertTrue(self.import_errors(source))

    def test_similar_absolute_system_name_is_not_a_child_package(self):
        self.assertTrue(self.import_errors('from systems.demo_extra.app import run'))

    def test_local_relative_and_absolute_imports_remain_allowed(self):
        for source, nested in [('from .app import run', False), ('from ..app import run', True), ('from systems.demo.app import run', False), ('from systems import demo', False)]:
            with self.subTest(source=source):
                self.assertEqual(self.import_errors(source, nested), [])

    def test_nested_sibling_system_is_refused(self):
        self.assertTrue(self.import_errors('from ...other.app import run', nested=True))
