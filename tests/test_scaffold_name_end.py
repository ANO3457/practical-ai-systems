import tempfile
import unittest
from pathlib import Path
from scripts.new_system import scaffold

class ScaffoldNameEnd(unittest.TestCase):
 def test_trailing_newline_is_refused_before_creating_any_output(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   with self.assertRaisesRegex(ValueError,"snake_case"):
    scaffold("demo\n","Demo","Beginner","Try it","Python",root=root)
   self.assertEqual(list(root.iterdir()),[])
 def test_valid_name_still_generates_the_named_system(self):
  with tempfile.TemporaryDirectory() as tmp:
   target=scaffold("demo_2","Demo","Beginner","Try it","Python",root=Path(tmp))
   self.assertEqual(target.name,"demo_2")
   self.assertTrue((target/"system.json").is_file())
