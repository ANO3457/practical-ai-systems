import ast
import json
import tempfile
import unittest
from pathlib import Path
from scripts.new_system import render, scaffold


class LiteralMetadata(unittest.TestCase):
    def test_replacement_values_are_not_recursively_interpreted(self):
        self.assertEqual(render("{{title}} / {{hook}}", {"title": "{{hook}}", "hook": "Guide"}), "{{hook}} / Guide")
        self.assertEqual(render("{{unknown}}", {"title": "Demo"}), "{{unknown}}")

    def test_scaffold_preserves_metadata_without_breaking_generated_formats(self):
        title = 'The """quoted""" <widget> & "{{hook}}"'
        hook = 'A <sample> & a backslash \\ plus a new\nline'
        with tempfile.TemporaryDirectory() as tmp:
            target = scaffold("literal_demo", title, "Beginner", hook, "Python", root=Path(tmp))
            source = (target / "app.py").read_text(encoding="utf-8")
            tree = ast.parse(source)
            self.assertIn(title, ast.get_docstring(tree))
            self.assertIn(hook, ast.get_docstring(tree))
            page = (target / "web/index.html").read_text(encoding="utf-8")
            self.assertIn("&lt;widget&gt;", page)
            self.assertIn("&lt;sample&gt;", page)
            self.assertNotIn("<widget>", page)
            comment = (target / "web/src/app.ts").read_text(encoding="utf-8").splitlines()[0]
            self.assertIn("{{hook}}", comment)
            self.assertEqual(json.loads((target / "system.json").read_text())["title"], title)
