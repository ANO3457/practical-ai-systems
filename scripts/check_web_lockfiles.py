"""Require reproducible npm lockfiles for every standalone system web app.

Run from the repository root: python3 scripts/check_web_lockfiles.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(root: Path = ROOT) -> int:
    errors = []
    packages = sorted((root / "systems").glob("*/web/package.json"))
    if not packages:
        errors.append("no systems/*/web/package.json files found")
    for package_path in packages:
        lock_path = package_path.with_name("package-lock.json")
        relative = package_path.relative_to(root)
        if not lock_path.is_file():
            errors.append(f"{relative.parent}: missing package-lock.json; run npm install --package-lock-only")
            continue
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{relative.parent}: cannot read package manifest/lock: {exc}")
            continue
        if not isinstance(package, dict) or not isinstance(lock, dict):
            errors.append(f"{relative.parent}: package manifest and lock must be JSON objects")
            continue
        version = lock.get("lockfileVersion", 0)
        if isinstance(version, bool) or not isinstance(version, int) or version < 2:
            errors.append(f"{relative.parent}: package-lock.json must use lockfileVersion 2 or newer")
            continue
        lock_packages = lock.get("packages")
        if not isinstance(lock_packages, dict) or not isinstance(lock_packages.get(""), dict):
            errors.append(f"{relative.parent}: package-lock.json needs an object root package record; regenerate it")
            continue
        root_package = lock_packages[""]
        for section in ("dependencies", "devDependencies", "optionalDependencies"):
            expected = package.get(section, {})
            actual = root_package.get(section, {})
            if not isinstance(expected, dict) or not isinstance(actual, dict):
                errors.append(f"{relative.parent}: {section} must be an object in both package manifest and lock")
                continue
            if expected != actual:
                errors.append(f"{relative.parent}: package-lock.json {section} do not match package.json; run npm install --package-lock-only")
    if errors:
        print("Web lockfile checks failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"All {len(packages)} standalone web apps have matching npm lockfiles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
