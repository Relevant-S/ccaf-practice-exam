#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Prepare the study map (or the decision map) for publishing as the learner's own artifact.

The Artifact tool wraps a page in its own <!doctype html><html><head>...<body>
skeleton, so the repo copy's outer wrapper is removed here. The result goes to
the learner's sanctum, never to the repo.

Usage:
    python build-map-artifact.py <project-root>            # study map
    python build-map-artifact.py <project-root> decision   # decision map

Prints the output path and the map version (MAP_VERSION in the page).

The two maps link to each other through a switch in their top bar. In the repo
the switch points at the other map's file. In the learner's copy it is pointed at
the learner's own published copy of the other map, read from BOND.md (the
"- **URL:**" line under "## Study Map" or "## Decision Map"). If that map isn't
published yet, the switch is left out, so it never leads to a dead file link.
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


def published_url(root: Path, heading: str) -> str | None:
    bond = root / "_bmad" / "memory" / "ccaf-tutor" / "BOND.md"
    if not bond.exists():
        return None
    text = bond.read_text(encoding="utf-8")
    section = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not section:
        return None
    url = re.search(r"\*\*URL:\*\*\s*(https://\S+)", section.group(1))
    return url.group(1) if url else None


def point_switch(text: str, root: Path, which: str) -> tuple[str, str]:
    if which == "decision":
        href, heading, link_id = "../study-map/ccaf-study-map.html", "Study Map", "to-study"
    else:
        href, heading, link_id = "../decision-map/ccaf-decision-map.html", "Decision Map", "to-decision"
    url = published_url(root, heading)
    if url:
        return text.replace(f'id="{link_id}" href="{href}"', f'id="{link_id}" href="{url}"'), url
    # Not published yet: drop the whole switch rather than link to a file the learner can't open.
    return re.sub(r'\n\s*<nav class="mapswitch".*?</nav>', "", text, count=1), "none (other map not published)"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python build-map-artifact.py <project-root> [decision]")
        sys.exit(1)
    root = Path(sys.argv[1]).resolve()
    which = sys.argv[2] if len(sys.argv) > 2 else "study"
    name = "ccaf-decision-map.html" if which == "decision" else "ccaf-study-map.html"
    source = root / ("decision-map" if which == "decision" else "study-map") / name
    if not source.exists():
        print(f"Map not found at {source}")
        sys.exit(1)

    lines = source.read_text(encoding="utf-8").splitlines()
    kept = [line for line in lines if line.strip() not in WRAPPER_LINES]
    text = "\n".join(kept) + "\n"

    text, switch = point_switch(text, root, which)
    match = re.search(r'const MAP_VERSION = "([^"]+)"', text)
    version = match.group(1) if match else "unknown"

    out = root / "_bmad" / "memory" / "ccaf-tutor" / "map" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"path: {out}")
    print(f"map_version: {version}")
    print(f"switch_to: {switch}")


if __name__ == "__main__":
    main()
