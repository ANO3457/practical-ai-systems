"""Enforce the contribution contract for every folder under ``systems/``.

Run ``python3 scripts/check_systems.py`` (CI runs it on every PR). Each rule
prints a fix-it hint so first-time contributors know exactly what to change.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.registry import REQUIRED_KEYS, load_manifests  # noqa: E402

NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
REQUIRED_FILES = ("__init__.py", "README.md", "system.json", "evaluate.py", "eval/cases.json", "eval/results.json")
REQUIRED_WEB_FILES = ("package.json", "tsconfig.json", "index.html", "serve.mjs", "src/app.ts", "src/app.test.ts", "src/main.ts")
README_SECTIONS = ("## Quickstart", "## Known limitations")
PLACEHOLDERS = ("TODO", "replace before submitting", "Placeholder logic")
STDLIB = set(sys.stdlib_module_names)


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            found.add(node.module)
    return found


def check_system(folder: Path) -> list[str]:
    name = folder.name
    errors = []
    if not NAME_RE.match(name):
        errors.append(f"{name}: folder name must be snake_case (letters, digits, underscores)")
    for rel in REQUIRED_FILES:
        if not (folder / rel).exists():
            errors.append(f"{name}: missing {rel} (see docs/ADDING_A_SYSTEM.md)")
    if not list(folder.glob("test_*.py")):
        errors.append(f"{name}: add at least one test_*.py unit test file")

    manifest = folder / "system.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        errors += [f"{name}: system.json missing '{key}'" for key in REQUIRED_KEYS if not data.get(key)]

    readme = folder / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        errors += [f"{name}: README.md needs a '{s}' section" for s in README_SECTIONS if s not in text]

    scanned = [p for p in folder.rglob("*") if p.is_file() and p.suffix in {".py", ".md", ".ts", ".html", ".json"}
               and "node_modules" not in p.parts and "dist" not in p.parts]
    for path in scanned:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for marker in PLACEHOLDERS:
            if marker in content:
                errors.append(f"{name}: {path.relative_to(folder)} still contains scaffold placeholder '{marker}'")

    for py in folder.rglob("*.py"):
        if "node_modules" in py.parts:
            continue
        for module in _imports(py):
            top = module.split(".")[0]
            if top == "systems" and not module.startswith(f"systems.{name}"):
                errors.append(f"{name}: {py.relative_to(folder)} imports {module}; systems must be standalone (copy the helper instead)")
            elif top == "common":
                errors.append(f"{name}: {py.relative_to(folder)} imports {module}; inline the helper so the system stays standalone")
            elif top not in STDLIB and top != "systems":
                errors.append(f"{name}: {py.relative_to(folder)} imports third-party '{top}'; systems use the standard library only")

    web = folder / "web"
    if web.exists():
        errors += [f"{name}: web/ missing {rel}" for rel in REQUIRED_WEB_FILES if not (web / rel).exists()]
        pkg = web / "package.json"
        if pkg.exists():
            deps = json.loads(pkg.read_text(encoding="utf-8")).get("dependencies", {})
            if deps:
                errors.append(f"{name}: web/package.json has runtime dependencies {sorted(deps)}; keep web apps zero-dependency")
        for ts in (web / "src").glob("*.ts"):
            for match in re.finditer(r"""from\s+["']([^"']+)["']""", ts.read_text(encoding="utf-8")):
                spec = match.group(1)
                if not (spec.startswith("./") or spec.startswith("node:")):
                    errors.append(f"{name}: web/src/{ts.name} imports '{spec}'; only ./local and node: imports are allowed")
    else:
        errors.append(f"{name}: missing web/ app (run scripts/new_system.py to scaffold one)")
    return errors


def check_all(root: Path = ROOT) -> list[str]:
    errors = []
    folders = sorted(p for p in (root / "systems").iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))
    try:
        load_manifests(root)
    except ValueError as exc:
        errors.append(str(exc))
    for folder in folders:
        errors += check_system(folder)
    return errors


def main() -> int:
    errors = check_all()
    if errors:
        print("Contribution checks failed:\n" + "\n".join(f"  - {e}" for e in errors), file=sys.stderr)
        return 1
    print(f"All {len(load_manifests())} systems satisfy the contribution contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
