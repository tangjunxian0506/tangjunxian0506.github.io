\
#!/usr/bin/env python3

import sys
from pathlib import Path

REQUIRED_QMD = ["index.qmd", "about.qmd", "project.qmd", "_quarto.yml"]
REQUIRED_HTML = ["index.html", "about.html", "project.html"]

def fail(msg: str, code: int = 1):
    print(f"FAIL: {msg}")
    sys.exit(code)

def main():
    repo = Path(".").resolve()

    # Check required source files exist
    for f in REQUIRED_QMD:
        if not (repo / f).exists():
            fail(f"Missing required file: {f}")

    # Check render output exists
    site_dir = repo / "_site"
    if not site_dir.exists():
        fail("Render output folder `_site/` not found. Did `quarto render` run successfully?")

    # Check required pages exist
    missing = [f for f in REQUIRED_HTML if not (site_dir / f).exists()]
    if missing:
        fail(f"Rendered site is missing required page(s): {', '.join(missing)}")

    # Basic content sanity: title present in index
    index_html = (site_dir / "index.html").read_text(encoding="utf-8", errors="ignore")
    if "<title" not in index_html.lower():
        fail("index.html does not appear to contain a <title> tag (unexpected).")

    print("PASS: Required files present and site rendered successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
