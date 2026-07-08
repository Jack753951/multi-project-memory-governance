#!/usr/bin/env python
"""Run governance validation and public-safety checks as one audit."""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import check_public_safety, validate_governance


def run_safety(root: Path) -> tuple[int, str]:
    old_argv = sys.argv[:]
    sys.argv = ["check_public_safety.py", str(root)]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = check_public_safety.main()
    finally:
        sys.argv = old_argv
    return code, buf.getvalue().strip()


def audit(root: Path) -> dict:
    validation_errors = validate_governance.validate(root)
    safety_code, safety_output = run_safety(root)
    recommendations = []
    if validation_errors:
        recommendations.append("Fix required governance files before delegating work to external agents.")
    if safety_code != 0:
        recommendations.append("Remove or redact private paths/tokens before public export.")
    if not (root / "docs").exists() and not (root / "notes").exists():
        recommendations.append("Add a project notes or docs namespace for durable rationale.")
    if not (root / "handoff" / "worker_tasks").exists():
        recommendations.append("Create handoff/worker_tasks/ for bounded external worker briefs.")
    if not recommendations:
        recommendations.append("No blocking governance issues found by the lightweight audit.")
    return {
        "root": str(root),
        "validation_passed": not validation_errors,
        "validation_errors": validation_errors,
        "public_safety_passed": safety_code == 0,
        "public_safety_output": safety_output,
        "recommendations": recommendations,
    }


def to_markdown(report: dict) -> str:
    lines = [
        "# Governance Audit",
        "",
        f"Root: `{report['root']}`",
        f"Validation: {'passed' if report['validation_passed'] else 'failed'}",
        f"Public safety: {'passed' if report['public_safety_passed'] else 'failed'}",
        "",
        "## Validation errors",
    ]
    if report["validation_errors"]:
        lines.extend(f"- {e}" for e in report["validation_errors"])
    else:
        lines.append("- None")
    lines.extend(["", "## Public safety output", "", "```text", report["public_safety_output"], "```", "", "## Recommendations"])
    lines.extend(f"- {r}" for r in report["recommendations"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".", help="Project directory to audit")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    report = audit(Path(args.target).resolve())
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(report), end="")
    return 0 if report["validation_passed"] and report["public_safety_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
