#!/usr/bin/env python
"""Inventory a handoff directory and suggest cleanup destinations without moving files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def classify(path: Path) -> str:
    name = path.name.lower()
    parts = {p.lower() for p in path.parts}
    if name == "index.md" or "memory_governance" in name or "active_strategy_queue" in name or "accepted_changes" in name:
        return "root-navigation"
    if "worker" in name or "worker_tasks" in parts:
        return "worker_tasks"
    if "review" in name or "reviews" in parts:
        return "reviews"
    if "archive" in parts or "superseded" in name:
        return "archive"
    if "unverified" in parts or "draft" in name:
        return "unverified"
    if path.suffix.lower() in {".log", ".json", ".txt"}:
        return "artifacts"
    return "inspect"


def plan(root: Path) -> dict:
    handoff = root / "handoff"
    entries = []
    if not handoff.exists():
        return {"root": str(root), "handoff_exists": False, "entries": [], "recommendations": ["Create handoff/ with INDEX.md, memory_governance.md, active_strategy_queue.md, and accepted_changes.md."]}
    for path in sorted(p for p in handoff.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        category = classify(path.relative_to(handoff))
        recommended = {
            "root-navigation": rel,
            "reviews": "handoff/reviews/",
            "worker_tasks": "handoff/worker_tasks/",
            "archive": "handoff/archive/",
            "unverified": "handoff/unverified/",
            "artifacts": "handoff/artifacts/",
            "inspect": "manual inspection",
        }[category]
        entries.append({"path": rel, "category": category, "recommended_destination": recommended})
    recommendations = [
        "Review the plan before moving files; this tool does not mutate the project.",
        "Keep INDEX.md, memory_governance.md, active_strategy_queue.md, and accepted_changes.md easy to find.",
        "Move bulky worker/review/log artifacts into class-level directories and link them from INDEX.md if still active.",
    ]
    return {"root": str(root), "handoff_exists": True, "entries": entries, "recommendations": recommendations}


def to_markdown(report: dict) -> str:
    lines = ["# Handoff Cleanup Plan", "", f"Root: `{report['root']}`", f"Handoff exists: {report['handoff_exists']}", ""]
    if report["entries"]:
        lines.extend(["| Path | Category | Recommended destination |", "|---|---|---|"])
        for item in report["entries"]:
            lines.append(f"| `{item['path']}` | {item['category']} | `{item['recommended_destination']}` |")
    else:
        lines.append("No handoff files found.")
    lines.extend(["", "## Recommendations"])
    lines.extend(f"- {item}" for item in report["recommendations"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    report = plan(Path(args.target).resolve())
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
