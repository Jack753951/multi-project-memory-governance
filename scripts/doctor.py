#!/usr/bin/env python
"""Check local environment and governance health."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import governance_audit


def doctor(root: Path) -> dict:
    audit = governance_audit.audit(root)
    checks = []
    checks.append({"name": "python_version", "passed": sys.version_info >= (3, 9), "detail": sys.version.split()[0]})
    checks.append({"name": "git_available", "passed": shutil.which("git") is not None, "detail": shutil.which("git") or "not found"})
    checks.append({"name": "governance_validation", "passed": audit["validation_passed"], "detail": audit["validation_errors"]})
    checks.append({"name": "public_safety", "passed": audit["public_safety_passed"], "detail": audit["public_safety_output"]})
    checks.append({"name": "worker_tasks_dir", "passed": (root / "handoff" / "worker_tasks").exists(), "detail": "handoff/worker_tasks"})
    checks.append({"name": "reviews_dir", "passed": (root / "handoff" / "reviews").exists(), "detail": "handoff/reviews"})
    return {"root": str(root), "passed": all(c["passed"] for c in checks), "checks": checks, "audit_recommendations": audit["recommendations"]}


def to_markdown(report: dict) -> str:
    lines = ["# MPMG Doctor", "", f"Root: `{report['root']}`", f"Overall: {'passed' if report['passed'] else 'failed'}", "", "## Checks"]
    for check in report["checks"]:
        mark = "PASS" if check["passed"] else "FAIL"
        lines.append(f"- {mark} `{check['name']}` — {check['detail']}")
    lines.extend(["", "## Recommendations"])
    lines.extend(f"- {item}" for item in report["audit_recommendations"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    report = doctor(Path(args.target).resolve())
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(report), end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
