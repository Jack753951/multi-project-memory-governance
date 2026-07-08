#!/usr/bin/env python
"""Validate worker task briefs and review artifacts for governance metadata."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

WORKER_REQUIRED = [
    "## Task",
    "## Required context reads",
    "## Allowed files/scope",
    "## Disallowed actions",
    "## Expected output",
    "## Validation",
]
REVIEW_REQUIRED = [
    "## Reviewer identity",
    "Reviewer route/tool:",
    "Visible runtime model:",
    "Provider / CLI version if visible:",
    "Review focus:",
    "Limitation:",
]


def check_file(path: Path, required: list[str]) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [item for item in required if item not in text]


def validate(root: Path) -> dict:
    handoff = root / "handoff"
    worker_dir = handoff / "worker_tasks"
    review_dir = handoff / "reviews"
    results = []
    if worker_dir.exists():
        for path in sorted(worker_dir.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            missing = check_file(path, WORKER_REQUIRED)
            results.append({"path": path.relative_to(root).as_posix(), "kind": "worker_task", "passed": not missing, "missing": missing})
    if review_dir.exists():
        for path in sorted(review_dir.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            missing = check_file(path, REVIEW_REQUIRED)
            results.append({"path": path.relative_to(root).as_posix(), "kind": "review", "passed": not missing, "missing": missing})
    recommendations = []
    if not results:
        recommendations.append("No worker task or review artifacts found. This is fine for a new project, but mature multi-agent workflows should keep bounded task and review artifacts.")
    failures = [item for item in results if not item["passed"]]
    if failures:
        recommendations.append("Patch failing artifacts before using them as future worker context or review evidence.")
    elif results:
        recommendations.append("Artifact metadata checks passed.")
    return {"root": str(root), "passed": not failures, "artifacts_checked": len(results), "results": results, "recommendations": recommendations}


def to_markdown(report: dict) -> str:
    lines = ["# Artifact Validation", "", f"Root: `{report['root']}`", f"Overall: {'passed' if report['passed'] else 'failed'}", f"Artifacts checked: {report['artifacts_checked']}", ""]
    if report["results"]:
        lines.extend(["| Path | Kind | Status | Missing |", "|---|---|---|---|"])
        for item in report["results"]:
            status = "PASS" if item["passed"] else "FAIL"
            missing = ", ".join(item["missing"]) if item["missing"] else ""
            lines.append(f"| `{item['path']}` | {item['kind']} | {status} | {missing} |")
        lines.append("")
    lines.append("## Recommendations")
    lines.extend(f"- {item}" for item in report["recommendations"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    report = validate(Path(args.target).resolve())
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(report), end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
