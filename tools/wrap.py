"""Turn a page written for a Claude artifact into a standalone HTML file for this site.

Artifact pages leave out the document skeleton (doctype, charset, viewport) because the artifact host adds it when
it publishes. A static host does not, so without this step the page renders in quirks mode with garbled characters.

    python tools/wrap.py SOURCE.html DEST.html
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BASE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
/* What the artifact host adds to every page; the page's own styles below override it. */
:root { color-scheme: light; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; }
img { max-width: 100%; }
[hidden] { display: none !important; }
/* Link back to the site's home page. System colors follow the page's light or dark scheme. */
.site-nav { padding: 8px max(16px, env(safe-area-inset-left, 0px)); font: 13px/1.4 system-ui, -apple-system, "Segoe UI", sans-serif;
  background: Canvas; color: CanvasText; border-bottom: 1px solid color-mix(in srgb, CanvasText 15%, transparent); }
.site-nav a { color: inherit; text-decoration: none; opacity: .75; }
.site-nav a:hover, .site-nav a:focus-visible { opacity: 1; text-decoration: underline; }
</style>
"""


def wrap(source: str, home: str) -> str:
    source = re.sub(r'<meta name="claude:[^"]*"[^>]*>\n?', "", source)
    end = source.find("</style>")
    if end < 0 or re.search(r"<!doctype|<html|<body", source[:2000], re.I):
        raise SystemExit("expected an artifact page: head tags and one <style> block first, no skeleton of its own")
    head, body = source[: end + len("</style>")], source[end + len("</style>"):]
    nav = f'<nav class="site-nav"><a href="{home}">&larr; Brian Chen &middot; Projects</a></nav>\n'
    return f"{BASE}{head}\n</head>\n<body>\n{nav}{body.lstrip()}\n</body>\n</html>\n"


if __name__ == "__main__":
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    depth = len(dest.resolve().relative_to(Path(__file__).resolve().parents[1]).parts) - 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(wrap(src.read_text(encoding="utf-8"), "../" * depth or "./"), encoding="utf-8")
    print(f"{src} -> {dest}")
