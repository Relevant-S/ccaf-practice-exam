#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Prepare the study map for publishing as the learner's own artifact.

The Artifact tool wraps a page in its own <!doctype html><html><head>...<body>
skeleton, so the repo copy's outer wrapper is removed here. The result goes to
the learner's sanctum, never to the repo.

Usage:
    python build-map-artifact.py <project-root>

Prints the output path and the map version (MAP_VERSION in the page).
"""

import re
import sys
from pathlib import Path

WRAPPER_LINES = [
    "<!doctype html>",
    '<html lang="en">',
    "<head>",
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
    "</head>",
    "<body>",
    "</body>",
    "</html>",
]


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python build-map-artifact.py <project-root>")
        sys.exit(1)
    root = Path(sys.argv[1]).resolve()
    source = root / "study-map" / "ccaf-study-map.html"
    if not source.exists():
        print(f"Study map not found at {source}")
        sys.exit(1)

    lines = source.read_text(encoding="utf-8").splitlines()
    kept = [line for line in lines if line.strip() not in WRAPPER_LINES]
    text = "\n".join(kept) + "\n"

    match = re.search(r'const MAP_VERSION = "([^"]+)"', text)
    version = match.group(1) if match else "unknown"

    out = root / "_bmad" / "memory" / "ccaf-tutor" / "map" / "ccaf-study-map.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"path: {out}")
    print(f"map_version: {version}")


if __name__ == "__main__":
    main()
