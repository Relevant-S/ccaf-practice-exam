#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
First Breath — Deterministic sanctum scaffolding for Richard (agent-ccaf-tutor).

Runs BEFORE the conversational awakening. Creates the sanctum folder structure,
copies template files with config values substituted, copies all reference files
into the sanctum, and auto-generates CAPABILITIES.md from capability prompt
frontmatter.

After this script runs, the sanctum is fully self-contained — the agent does
not depend on the skill bundle location for normal operation.

Usage:
    python3 init-sanctum.py <project-root> <skill-path> [--reset | --refresh]

    project-root: The root of the project (where _bmad/ lives)
    skill-path:   Path to the skill directory (where SKILL.md, references/, assets/ live)
    --reset:      If the sanctum already exists, archive it (rename to
                  ccaf-tutor.archive-YYYY-MM-DD-HHMMSS) before scaffolding fresh.
                  Existing data is preserved on disk; the user can restore by
                  renaming the archive folder back.
    --refresh:    If the sanctum already exists, re-copy references/ and scripts/
                  from the skill and regenerate CAPABILITIES.md. Learner files
                  (PERSONA, CREED, BOND, MEMORY, mastery, history, sessions,
                  generated questions) are not touched. Use this after the skill
                  has been updated, so an existing sanctum picks up the changes.
"""

import sys
import re
import shutil
from datetime import date, datetime
from pathlib import Path

# --- Agent-specific configuration ---

SKILL_NAME = "agent-ccaf-tutor"
# Sanctum dir uses the agent's `code` (from customize.toml), not the full skill folder name.
# This keeps the per-user memory path tidy: _bmad/memory/ccaf-tutor/ instead of agent-ccaf-tutor/.
SANCTUM_DIR = "ccaf-tutor"

# Files that stay in the skill bundle (only used during First Breath, never copied to sanctum)
SKILL_ONLY_FILES = {"first-breath.md"}

# Templates copied from assets/ into the sanctum on first run.
# Each "<name>-template.md" becomes "<NAME>.md" in the sanctum (uppercased, with hyphens kept).
TEMPLATE_FILES = [
    "PERSONA-template.md",
    "CREED-template.md",
    "BOND-template.md",
    "MEMORY-template.md",
    "INDEX-template.md",
    "topics-mastery-template.md",
    "question-history-template.md",
    "misconceptions-template.md",
    "practical-tasks-template.md",
]

# Whether the owner can teach this agent new capabilities (Richard is fixed).
EVOLVABLE = False

# --- End agent-specific configuration ---


def parse_toml_config(config_path: Path) -> dict:
    """Minimal TOML parser for top-level [section] scalar values.

    Reads keys like `user_name = "Alex"` from `[core]` and other sections,
    flattening into a single dict. Sufficient for the few config keys this
    script needs (user_name, communication_language).
    """
    config = {}
    if not config_path.exists():
        return config
    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("["):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                value = value.strip().strip("'\"")
                if value:
                    config[key.strip()] = value
    return config


def parse_yaml_config(config_path: Path) -> dict:
    """Simple YAML key-value parser. Handles top-level scalar values only."""
    config = {}
    if not config_path.exists():
        return config
    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, _, value = line.partition(":")
                value = value.strip().strip("'\"")
                if value:
                    config[key.strip()] = value
    return config


def parse_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    meta = {}
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return meta

    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("'\"")
    return meta


def copy_references(source_dir: Path, dest_dir: Path) -> list[str]:
    """Copy all reference files (except skill-only files) into the sanctum."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []

    for source_file in sorted(source_dir.iterdir()):
        if source_file.name in SKILL_ONLY_FILES:
            continue
        if source_file.is_file():
            shutil.copy2(source_file, dest_dir / source_file.name)
            copied.append(source_file.name)

    return copied


def copy_scripts(source_dir: Path, dest_dir: Path) -> list[str]:
    """Copy any scripts the capabilities might use into the sanctum."""
    if not source_dir.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []

    for source_file in sorted(source_dir.iterdir()):
        if source_file.is_file() and source_file.name != "init-sanctum.py":
            shutil.copy2(source_file, dest_dir / source_file.name)
            copied.append(source_file.name)

    return copied


def discover_capabilities(references_dir: Path, sanctum_refs_path: str) -> list[dict]:
    """Scan references/ for capability prompt files with frontmatter."""
    capabilities = []

    for md_file in sorted(references_dir.glob("*.md")):
        if md_file.name in SKILL_ONLY_FILES:
            continue
        meta = parse_frontmatter(md_file)
        if meta.get("name") and meta.get("code"):
            capabilities.append({
                "name": meta["name"],
                "description": meta.get("description", ""),
                "code": meta["code"],
                "source": f"{sanctum_refs_path}/{md_file.name}",
            })
    return capabilities


def generate_capabilities_md(capabilities: list[dict], evolvable: bool) -> str:
    """Generate CAPABILITIES.md content from discovered capabilities."""
    lines = [
        "# Capabilities",
        "",
        "## Built-in",
        "",
        "| Code | Name | Description | Source |",
        "|------|------|-------------|--------|",
    ]
    for cap in capabilities:
        lines.append(
            f"| [{cap['code']}] | {cap['name']} | {cap['description']} | `{cap['source']}` |"
        )

    if evolvable:
        lines.extend([
            "",
            "## Learned",
            "",
            "_Capabilities added by the owner over time. Prompts live in `capabilities/`._",
            "",
            "| Code | Name | Description | Source | Added |",
            "|------|------|-------------|--------|-------|",
            "",
            "## How to Add a Capability",
            "",
            'Tell me "I want you to be able to do X" and we\'ll create it together.',
            "I'll write the prompt, save it to `capabilities/`, and register it here.",
            "Next session, I'll know how.",
            "Load `./references/capability-authoring.md` for the full creation framework.",
        ])

    lines.extend([
        "",
        "## Tools",
        "",
        "Prefer crafting your own tools over depending on external ones. A script you wrote "
        "and saved is more reliable than an external API. Use the file system creatively.",
        "",
        "### User-Provided Tools",
        "",
        "_MCP servers, APIs, or services the owner has made available. Document them here._",
    ])

    return "\n".join(lines) + "\n"


def substitute_vars(content: str, variables: dict) -> str:
    """Replace {var_name} placeholders with values from the variables dict."""
    for key, value in variables.items():
        content = content.replace(f"{{{key}}}", value)
    return content


def main():
    args = sys.argv[1:]
    reset = "--reset" in args
    refresh = "--refresh" in args
    args = [a for a in args if a not in ("--reset", "--refresh")]

    if len(args) < 2 or (reset and refresh):
        print("Usage: python3 init-sanctum.py <project-root> <skill-path> [--reset | --refresh]")
        sys.exit(1)

    project_root = Path(args[0]).resolve()
    skill_path = Path(args[1]).resolve()

    # Paths
    bmad_dir = project_root / "_bmad"
    memory_dir = bmad_dir / "memory"
    sanctum_path = memory_dir / SANCTUM_DIR
    assets_dir = skill_path / "assets"
    references_dir = skill_path / "references"
    scripts_dir = skill_path / "scripts"

    # Sanctum subdirectories
    sanctum_refs = sanctum_path / "references"
    sanctum_scripts = sanctum_path / "scripts"

    # Fully qualified path for CAPABILITIES.md references
    sanctum_refs_path = "./references"

    # Check if sanctum already exists
    if refresh:
        if not sanctum_path.exists():
            print(f"No sanctum at {sanctum_path} — nothing to refresh. Run without --refresh first.")
            sys.exit(1)
        copied_refs = copy_references(references_dir, sanctum_refs)
        copied_scripts = copy_scripts(scripts_dir, sanctum_scripts)
        capabilities = discover_capabilities(references_dir, sanctum_refs_path)
        (sanctum_path / "CAPABILITIES.md").write_text(
            generate_capabilities_md(capabilities, evolvable=EVOLVABLE), encoding="utf-8"
        )
        print(f"Refreshed sanctum at {sanctum_path}")
        print(f"  Re-copied {len(copied_refs)} reference files and {len(copied_scripts)} scripts")
        print(f"  Regenerated CAPABILITIES.md ({len(capabilities)} built-in capabilities)")
        print("  Learner files were not touched.")
        sys.exit(0)

    if sanctum_path.exists():
        if reset:
            timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            archive_path = sanctum_path.parent / f"{SANCTUM_DIR}.archive-{timestamp}"
            sanctum_path.rename(archive_path)
            print(f"Archived existing sanctum to {archive_path}")
            print("To restore later, rename the archive folder back to its original name.")
            print()
        else:
            print(f"Sanctum already exists at {sanctum_path}")
            print("This agent has already been born. Skipping First Breath scaffolding.")
            print("To pick up skill updates, re-run with --refresh (learner files are kept).")
            print("To start fresh, re-run with --reset (existing sanctum will be archived, not deleted).")
            sys.exit(0)

    # Load config — try TOML first (current BMad convention), fall back to YAML
    config = {}
    for config_file in ["config.toml", "config.user.toml"]:
        config.update(parse_toml_config(bmad_dir / config_file))
    for config_file in ["config.yaml", "config.user.yaml"]:
        config.update(parse_yaml_config(bmad_dir / config_file))

    # Build variable substitution map
    today = date.today().isoformat()
    variables = {
        "user_name": config.get("user_name", "friend"),
        "communication_language": config.get("communication_language", "English"),
        "birth_date": today,
        "project_root": str(project_root),
        "sanctum_path": str(sanctum_path),
    }

    # Create sanctum structure
    sanctum_path.mkdir(parents=True, exist_ok=True)
    (sanctum_path / "sessions").mkdir(exist_ok=True)
    (sanctum_path / "generated-questions").mkdir(exist_ok=True)
    print(f"Created sanctum at {sanctum_path}")

    # Copy reference files (capability prompts + memory-guidance) into sanctum
    copied_refs = copy_references(references_dir, sanctum_refs)
    print(f"  Copied {len(copied_refs)} reference files to sanctum/references/")
    for name in copied_refs:
        print(f"    - {name}")

    # Copy any supporting scripts into sanctum (excluding init-sanctum.py itself)
    copied_scripts = copy_scripts(scripts_dir, sanctum_scripts)
    if copied_scripts:
        print(f"  Copied {len(copied_scripts)} scripts to sanctum/scripts/")
        for name in copied_scripts:
            print(f"    - {name}")

    # Copy and substitute template files
    for template_name in TEMPLATE_FILES:
        template_path = assets_dir / template_name
        if not template_path.exists():
            print(f"  Warning: template {template_name} not found, skipping")
            continue

        # Remove "-template" from the output filename and uppercase it
        output_name = template_name.replace("-template", "").upper()
        # Fix extension casing: .MD -> .md
        output_name = output_name[:-3] + ".md"

        content = template_path.read_text(encoding="utf-8")
        content = substitute_vars(content, variables)

        output_path = sanctum_path / output_name
        output_path.write_text(content, encoding="utf-8")
        print(f"  Created {output_name}")

    # Auto-generate CAPABILITIES.md from references/ frontmatter
    capabilities = discover_capabilities(references_dir, sanctum_refs_path)
    capabilities_content = generate_capabilities_md(capabilities, evolvable=EVOLVABLE)
    (sanctum_path / "CAPABILITIES.md").write_text(capabilities_content, encoding="utf-8")
    print(f"  Created CAPABILITIES.md ({len(capabilities)} built-in capabilities discovered)")

    print()
    print("First Breath scaffolding complete.")
    print("The conversational awakening can now begin.")
    print(f"Sanctum: {sanctum_path}")


if __name__ == "__main__":
    main()
