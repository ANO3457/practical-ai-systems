import tempfile
import unittest
from pathlib import Path
from scripts.build_site import build

class SiteOutputSourceGuard(unittest.TestCase):
 def test_source_paths_are_refused_before_any_deletion(self):
  for relative in (".","systems","systems/demo","scripts","tests","docs"):
   with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)/"repo";root.mkdir();(root/"systems").mkdir()
    out=root/relative;out.mkdir(parents=True,exist_ok=True)
    sentinel=out/"keep.txt";sentinel.write_text("source")
    with self.assertRaisesRegex(ValueError,"output"):
     build(out,root=root)
    self.assertEqual(sentinel.read_text(),"source")
 def test_normal_output_directory_is_rebuilt(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"repo";root.mkdir();(root/"systems").mkdir()
   out=root/"site";out.mkdir();(out/"stale.txt").write_text("old output")
   self.assertEqual(build(out,root=root),[])
   self.assertFalse((out/"stale.txt").exists())
   self.assertTrue((out/"index.html").is_file())

class MissingBuildPreservesOutput(unittest.TestCase):
 def test_missing_browser_build_preserves_previous_gallery(self):
  import json
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/"repo";folder=root/"systems/demo";folder.mkdir(parents=True)
   (folder/"system.json").write_text(json.dumps({"title":"Demo","level":"Beginner","order":1,"prerequisites":"Python","hook":"Demo"}))
   out=root/"site";out.mkdir();sentinel=out/"keep.txt";sentinel.write_text("previous gallery")
   with self.assertRaises(FileNotFoundError):build(out,root=root)
   self.assertEqual(sentinel.read_text(),"previous gallery")
