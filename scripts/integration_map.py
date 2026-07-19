#!/usr/bin/env python
"""Inspect an existing AI-assisted repo and map its context surfaces without changing it."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".tox",
    ".venv",
    ".cache",
    ".gradle",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    "venv",
    "node_modules",
    "coverage",
    "dist",
    "build",
    "out",
    "target",
    "vendor",
    "__pycache__",
}

DEFAULT_WRITE = "__mpmg_default_write__"

FILE_SURFACES = {
    "AGENTS.md": ("repo-instructions", "Repository or directory-scoped agent instructions"),
    "CLAUDE.md": ("repo-instructions", "Claude Code project instructions"),
    "CLAUDE.local.md": ("local-instructions", "Local Claude Code instructions; usually not shared project truth"),
    ".cursorrules": ("repo-instructions", "Cursor project instructions"),
    "copilot-instructions.md": ("repo-instructions", "GitHub Copilot repository instructions"),
    "ruler.toml": ("instruction-sync", "Cross-agent instruction synchronization configuration"),
}

DIRECTORY_SURFACES = {
    ".claude/rules": ("repo-instructions", "Path-scoped Claude Code rules"),
    ".cursor/rules": ("repo-instructions", "Cursor project rules"),
    ".ruler": ("instruction-sync", "Cross-agent instruction source"),
    ".sopify": ("workflow-handoff", "Plans, decisions, handoffs, or verification evidence"),
    ".specify": ("specification", "Spec Kit workflow artifacts"),
    "openspec": ("specification", "OpenSpec change and specification artifacts"),
    ".bmad-core": ("workflow-handoff", "BMAD workflow and agent artifacts"),
    "_bmad": ("workflow-handoff", "BMAD workflow and agent artifacts"),
    "handoff": ("workflow-handoff", "Repository-local handoff and accepted work state"),
    ".obsidian": ("project-notes", "Obsidian vault configuration; nearby notes may hold long-term rationale"),
}

MEMORY_BANK_FILES = {
    "projectbrief.md",
    "productcontext.md",
    "activecontext.md",
    "systempatterns.md",
    "techcontext.md",
    "progress.md",
}

OVERLAY_MARKERS = {
    ".mpmg/authority-map.md",
    ".mpmg/authority-map.json",
    "handoff/memory_governance.md",
}

ROLE_GUIDANCE = {
    "repo-instructions": "Normative agent instructions. Keep scope explicit; do not use as a rolling progress log.",
    "local-instructions": "Operator-local instructions. Do not assume teammates or external workers can see them.",
    "instruction-sync": "Distribution mechanism for instructions. Synchronization does not make a rule authoritative at every scope.",
    "workflow-handoff": "Current work state, decisions, or evidence. Name one current owner and define freshness.",
    "specification": "Intended behavior and accepted requirements. Treat divergence from live implementation as drift to resolve.",
    "project-memory": "Durable project context. Verify changing facts before using them as current state.",
    "project-notes": "Long-term rationale and research. Link to current repo truth instead of duplicating it.",
    "mpmg-overlay": "Authority map between existing context systems; it should not become another project database.",
}


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _walk(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        yield Path(current), dirs, sorted(files)


def _add_surface(
    found: dict[tuple[str, str], dict[str, Any]],
    *,
    name: str,
    kind: str,
    path: str,
    description: str,
) -> None:
    key = (name, kind)
    item = found.setdefault(
        key,
        {
            "name": name,
            "kind": kind,
            "paths": [],
            "description": description,
            "guidance": ROLE_GUIDANCE[kind],
        },
    )
    if path not in item["paths"]:
        item["paths"].append(path)


def inspect(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"target is not a directory: {root}")

    found: dict[tuple[str, str], dict[str, Any]] = {}
    memory_candidates: dict[Path, set[str]] = {}

    for current, dirs, files in _walk(root):
        rel_dir = _rel(current, root) if current != root else ""

        for dirname in dirs:
            rel = f"{rel_dir}/{dirname}".strip("/")
            marker = next(
                (candidate for candidate in DIRECTORY_SURFACES if rel == candidate or rel.endswith(f"/{candidate}")),
                None,
            )
            if marker:
                kind, description = DIRECTORY_SURFACES[marker]
                _add_surface(found, name=marker, kind=kind, path=rel, description=description)

        for filename in files:
            path = current / filename
            lower = filename.lower()
            rel = _rel(path, root)

            if filename in FILE_SURFACES:
                kind, description = FILE_SURFACES[filename]
                _add_surface(found, name=filename, kind=kind, path=rel, description=description)
            elif rel == ".github/copilot-instructions.md":
                kind, description = FILE_SURFACES["copilot-instructions.md"]
                _add_surface(found, name="copilot-instructions.md", kind=kind, path=rel, description=description)

            if lower in MEMORY_BANK_FILES:
                memory_candidates.setdefault(current, set()).add(lower)

            if any(rel == marker or rel.endswith(f"/{marker}") for marker in OVERLAY_MARKERS):
                _add_surface(
                    found,
                    name="MPMG authority overlay",
                    kind="mpmg-overlay",
                    path=rel,
                    description="Existing authority-boundary declaration",
                )

    for directory, names in memory_candidates.items():
        if len(names) >= 2 or "activecontext.md" in names:
            _add_surface(
                found,
                name="Cline-style memory bank",
                kind="project-memory",
                path=_rel(directory, root) or ".",
                description=f"Structured project memory ({len(names)} common memory-bank files detected)",
            )

    surfaces = sorted(found.values(), key=lambda item: (item["kind"], item["name"].lower()))
    for item in surfaces:
        item["paths"].sort()

    kinds = {item["kind"] for item in surfaces}
    questions = [
        "Which source owns current observed state, and how is its freshness verified?",
        "Which source owns intended behavior when specifications and implementation diverge?",
        "Which instructions are global, repository-scoped, directory-scoped, or operator-local?",
        "What must an external worker read explicitly before acting?",
        "Which memory sources are recall aids only and must be re-verified?",
    ]
    if "workflow-handoff" not in kinds:
        questions.append("No repository-local handoff surface was detected; decide whether the project needs one.")
    if "repo-instructions" not in kinds:
        questions.append("No shared repository instruction file was detected; decide how agents discover project rules.")

    return {
        "schema_version": 1,
        "status": "proposed-not-authoritative",
        "root": str(root),
        "read_only": True,
        "purpose": "Map existing context systems so they can coexist without silently competing for authority.",
        "detected_surfaces": surfaces,
        "overlay_contract": {
            "task_authority": "Current explicit user or operator instruction defines the task and scope; it does not rewrite observed facts.",
            "current_observed_state": "Live files, configuration, and fresh validation evidence.",
            "intended_behavior": "Current accepted requirements, specifications, and policies; divergence from implementation is drift to resolve, not a reason to silently discard either side.",
            "current_work_state": "One explicitly named repo-local handoff or workflow owner.",
            "long_term_rationale": "Project notes or decision records that link back to current repo truth.",
            "memory": "Recall and discovery unless the fact is stable and its scope is explicit.",
            "external_workers": "Receive explicit required reads, scope, expected output, and validation; inheritance is never assumed.",
        },
        "questions_to_resolve": questions,
        "limitations": [
            "Detection is path- and filename-based; it does not prove that a file is current, correct, or actually read by an agent.",
            "External memory backends and runtime policy systems may not leave repository-local markers and cannot be inferred reliably.",
            "The report proposes roles, not semantic truth. A human or project owner must resolve real conflicts.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# AI Context Integration Map",
        "",
        f"Root: `{report['root']}`",
        f"Status: `{report['status']}`",
        "Mode: read-only inspection",
        "",
        f"> {report['purpose']}",
        "",
        "## Detected context surfaces",
        "",
    ]
    surfaces = report["detected_surfaces"]
    if not surfaces:
        lines.append("No known context surfaces detected.")
    else:
        lines.extend(["| Surface | Kind | Paths | Suggested role |", "|---|---|---|---|"])
        for item in surfaces:
            paths = "<br>".join(f"`{path}`" for path in item["paths"])
            lines.append(f"| {item['name']} | `{item['kind']}` | {paths} | {item['guidance']} |")

    lines.extend(["", "## Thin overlay contract", ""])
    labels = {
        "task_authority": "Task authority",
        "current_observed_state": "Current observed state",
        "intended_behavior": "Intended behavior",
        "current_work_state": "Current work state",
        "long_term_rationale": "Long-term rationale",
        "memory": "Memory",
        "external_workers": "External workers",
    }
    for key, value in report["overlay_contract"].items():
        lines.append(f"- **{labels[key]}:** {value}")

    lines.extend(["", "## Questions the project owner must resolve", ""])
    lines.extend(f"- [ ] {question}" for question in report["questions_to_resolve"])
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument(
        "--write",
        nargs="?",
        const=DEFAULT_WRITE,
        help="Optionally write the report under the target; omitted means stdout only.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing --write path")
    args = parser.parse_args(argv)

    root = Path(args.target).resolve()
    try:
        report = inspect(root)
    except ValueError as exc:
        parser.error(str(exc))

    if args.write:
        if args.write == DEFAULT_WRITE:
            suffix = "json" if args.format == "json" else "md"
            write_value = f".mpmg/authority-map.{suffix}"
        else:
            write_value = args.write
        destination = Path(write_value)
        if not destination.is_absolute():
            destination = root / destination
        destination = destination.resolve()
        try:
            destination.relative_to(root)
        except ValueError:
            parser.error(f"--write path must stay inside target: {destination}")
        if destination.is_dir():
            parser.error(f"--write path is a directory: {destination}")
        if destination.exists() and not args.force:
            parser.error(f"refusing to overwrite existing file: {destination}; use --force")
        saved_report = dict(report)
        saved_report["root"] = "."
        text = json.dumps(saved_report, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else render_markdown(saved_report)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8", newline="\n")
        print(f"write {destination}")
    else:
        text = json.dumps(report, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else render_markdown(report)
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
