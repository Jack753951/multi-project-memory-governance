#!/usr/bin/env python
"""Unified CLI for Multi-Project Memory Governance."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import (
    check_public_safety,
    doctor,
    export_public_subset,
    governance_audit,
    init_governance,
    new_worker_task,
    plan_handoff_cleanup,
    validate_governance,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="Initialize governance files in a target project")
    p.add_argument("--target", default=".")
    p.add_argument("--project-name", required=True)
    p.add_argument("--notes-namespace", required=True)
    p.add_argument("--context-file", default=".hermes.md")
    p.add_argument("--force", action="store_true")

    p = sub.add_parser("validate", help="Validate governance layout")
    p.add_argument("target", nargs="?", default=".")

    p = sub.add_parser("audit", help="Run validation and public-safety checks")
    p.add_argument("target", nargs="?", default=".")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")

    p = sub.add_parser("safety-scan", help="Scan for obvious public-safety issues")
    p.add_argument("target", nargs="?", default=".")

    p = sub.add_parser("doctor", help="Check local environment and governance health")
    p.add_argument("target", nargs="?", default=".")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")

    p = sub.add_parser("worker-task", help="Generate a bounded worker task")
    p.add_argument("--target", default=".")
    p.add_argument("--name", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--scope", action="append", default=[])
    p.add_argument("--read", action="append", default=[])
    p.add_argument("--validation", default="<validation command>")
    p.add_argument("--worker-tool", default="<worker-tool>")
    p.add_argument("--model", default="not exposed by tool")
    p.add_argument("--provider-version", default="not exposed")
    p.add_argument("--focus", default="mixed")
    p.add_argument("--limitation", default="Task brief generated before worker execution.")
    p.add_argument("--output")
    p.add_argument("--force", action="store_true")

    p = sub.add_parser("export-public", help="Create a sanitized public subset export")
    p.add_argument("--output", required=True)
    p.add_argument("--force", action="store_true")

    p = sub.add_parser("plan-handoff-cleanup", help="Inventory handoff and suggest cleanup destinations")
    p.add_argument("target", nargs="?", default=".")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")

    args = parser.parse_args(argv)
    if args.command == "init":
        return init_governance.main(["--target", args.target, "--project-name", args.project_name, "--notes-namespace", args.notes_namespace, "--context-file", args.context_file] + (["--force"] if args.force else []))
    if args.command == "validate":
        return validate_governance.main([args.target])
    if args.command == "audit":
        return governance_audit.main([args.target, "--format", args.format])
    if args.command == "safety-scan":
        return check_public_safety.main_for_path(Path(args.target).resolve())
    if args.command == "doctor":
        return doctor.main([args.target, "--format", args.format])
    if args.command == "worker-task":
        forwarded = ["--target", args.target, "--name", args.name, "--task", args.task, "--validation", args.validation, "--worker-tool", args.worker_tool, "--model", args.model, "--provider-version", args.provider_version, "--focus", args.focus, "--limitation", args.limitation]
        for item in args.scope:
            forwarded.extend(["--scope", item])
        for item in args.read:
            forwarded.extend(["--read", item])
        if args.output:
            forwarded.extend(["--output", args.output])
        if args.force:
            forwarded.append("--force")
        return new_worker_task.main(forwarded)
    if args.command == "export-public":
        return export_public_subset.main(["--output", args.output] + (["--force"] if args.force else []))
    if args.command == "plan-handoff-cleanup":
        return plan_handoff_cleanup.main([args.target, "--format", args.format])
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
