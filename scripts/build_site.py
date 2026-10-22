"""Assemble a static gallery of every system's web app into ``site/``.

Prerequisite: each ``systems/<name>/web`` has been built (``npm run build``).
Usage: python3 scripts/build_site.py [--out site] [--repo-url URL]
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.registry import LEVELS, load_manifests  # noqa: E402

DEFAULT_REPO = "https://github.com/shivamnegi92/practical-ai-systems"


def build(out: Path, repo_url: str = DEFAULT_REPO, root: Path = ROOT) -> list[str]:
    root, out = root.resolve(), out.resolve()
    protected = [root / name for name in ("systems", "scripts", "templates", "tests", "docs", "common", "examples", "catalog", ".git", ".github")]
    if out == root or out in root.parents or any(out == path or path in out.parents for path in protected):
        raise ValueError("output directory must not overlap repository source directories")
    manifests = load_manifests(root)
    for name in manifests:
        web = root / "systems" / name / "web"
        for asset in (web / "dist" / "main.js", web / "index.html"):
            if not asset.is_file():
                raise FileNotFoundError(f"{name}: {asset} missing; build the web app first")
    index_page = render_index(manifests, root, repo_url)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    built = []
    for name in manifests:
        web = root / "systems" / name / "web"
        if not (web / "dist" / "main.js").exists():
            raise FileNotFoundError(f"{name}: web/dist/main.js missing; run 'npm run build' in {web}")
        dest = out / name
        shutil.copytree(web / "dist", dest / "dist", ignore=shutil.ignore_patterns("*.test.js"))
        page = (web / "index.html").read_text(encoding="utf-8")
        page = page.replace('href="../README.md"', f'href="{repo_url}/blob/main/systems/{name}/README.md"')
        page = page.replace("<body>", '<body>\n  <p><a href="../">&larr; All systems</a></p>', 1)
        (dest / "index.html").write_text(page, encoding="utf-8")
        built.append(name)
    (out / "index.html").write_text(index_page, encoding="utf-8")
    (out / ".nojekyll").write_text("")
    return built


def _metric_summary(root: Path, name: str) -> str:
    results = json.loads((root / "systems" / name / "eval" / "results.json").read_text())
    cases = results["dataset"]["cases"]
    return f"{cases} synthetic cases"


def render_index(manifests: dict[str, dict], root: Path, repo_url: str) -> str:
    sections = []
    for level in LEVELS:
        cards = []
        for name, m in manifests.items():
            if m["level"] != level:
                continue
            cards.append(
                f'<li class="card"><h3><a href="{name}/">{html.escape(m["title"])}</a></h3>'
                f'<p>{html.escape(m["hook"])}</p>'
                f'<p class="meta">{_metric_summary(root, name)} · '
                f'<a href="{repo_url}/tree/main/systems/{name}">Source</a></p></li>'
            )
        sections.append(f'<section aria-labelledby="{level.lower()}"><h2 id="{level.lower()}">{level}</h2>'
                        f'<ul class="grid">{"".join(cards)}</ul></section>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Practical AI Systems: try every project in your browser</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1080px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; line-height: 1.5; }}
  .grid {{ list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }}
  .card {{ border: 1px solid #ccc; border-radius: 8px; padding: 1rem; }}
  .card h3 {{ margin: 0 0 .5rem; font-size: 1.05rem; }}
  .meta {{ font-size: .85rem; color: #444; }}
  a {{ color: #1d4ed8; }} a:focus-visible {{ outline: 3px solid #1d4ed8; outline-offset: 2px; }}
</style>
</head>
<body>
<main>
  <h1>Practical AI Systems</h1>
  <p>{len(manifests)} small, honest AI systems you can run right here: no install, no API key, nothing leaves your browser.
  Each one has a Python version, tests, an evaluation, and documented limitations.
  <a href="{repo_url}">View on GitHub</a> · <a href="{repo_url}/blob/main/CONTRIBUTING.md">Contribute a system</a></p>
  {"".join(sections)}
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "site")
    parser.add_argument("--repo-url", default=DEFAULT_REPO)
    args = parser.parse_args()
    try:
        built = build(args.out, args.repo_url)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Built gallery with {len(built)} systems at {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
