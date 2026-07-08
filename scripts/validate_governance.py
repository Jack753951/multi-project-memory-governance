#!/usr/bin/env python
"""Validate a project using the memory-governance layout."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED = [
    "handoff/memory_governance.md",
    "handoff/active_strategy_queue.md",
    "handoff/INDEX.md",
    "handoff/accepted_changes.md",
]
REQUIRED_PHRASES = {
    "handoff/memory_governance.md": ["Authority order", "Global durable memory", "External workers"],
    "handoff/active_strategy_queue.md": ["Active gates", "Memory routing reminder"],
    "handoff/INDEX.md": ["Read first"],
}
UNFILLED_PLACEHOLDERS = ["<project-name>", "<project-notes-namespace>", "<project-context-file>", "<project-notes-index>"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED:
        path = root / rel
        if not path.exists():
            errors.append(f"missing required file: {rel}")
            continue
        text = read(path)
        for phrase in REQUIRED_PHRASES.get(rel, []):
            if phrase not in text:
                errors.append(f"{rel}: missing phrase {phrase!r}")
        for placeholder in UNFILLED_PLACEHOLDERS:
            if placeholder in text:
                errors.append(f"{rel}: unfilled placeholder {placeholder}")

    context_candidates = [root / ".hermes.md", root / "AGENTS.md", root / "CLAUDE.md"]
    if not any(p.exists() for p in context_candidates):
        errors.append("missing project context file: expected .hermes.md, AGENTS.md, or CLAUDE.md")
    else:
        context_text = "\n".join(read(p) for p in context_candidates if p.exists())
        if "Required reads" not in context_text:
            errors.append("project context: missing 'Required reads' section")
        if "global durable memory" not in context_text.lower():
            errors.append("project context: should state external workers/global durable memory boundary")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".", help="Project directory to validate")
    args = parser.parse_args(argv)
    root = Path(args.target).resolve()
    errors = validate(root)
    if errors:
        print("Governance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Governance validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
