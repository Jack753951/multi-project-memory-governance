#!/usr/bin/env python
"""Generate a bounded worker-task handoff file."""
from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    return value.strip("-") or "worker-task"


def render(template: str, args: argparse.Namespace) -> str:
    scope = "\n".join(f"- `{item.strip()}`" for item in args.scope if item.strip()) or "- `<path>`"
    reads = "\n".join(f"- `{item.strip()}`" for item in args.read if item.strip())
    if reads:
        reads = "- `.hermes.md`\n- `handoff/memory_governance.md`\n- `handoff/active_strategy_queue.md`\n" + reads
    else:
        reads = "- `.hermes.md`\n- `handoff/memory_governance.md`\n- `handoff/active_strategy_queue.md`"
    text = template
    text = text.replace("<short-name>", args.name)
    text = text.replace("<What to accomplish.>", args.task)
    text = re.sub(r"- `<project-context-file>`\n- `handoff/memory_governance.md`\n- `handoff/active_strategy_queue.md`\n- `<specific artifact for this task>`", reads, text)
    text = text.replace("- `<path>`", scope)
    text = text.replace("<validation command>", args.validation)
    text = text.replace("<worker-tool>", args.worker_tool)
    text = text.replace("<model if exposed, else not exposed by tool>", args.model)
    text = text.replace("<value or not exposed>", args.provider_version)
    text = text.replace("<engineering | strategy | safety | UX | mixed>", args.focus)
    text = text.replace("<what was not inspected or unavailable>", args.limitation)
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Target project directory")
    parser.add_argument("--name", required=True, help="Short task name")
    parser.add_argument("--task", required=True, help="Task objective")
    parser.add_argument("--scope", action="append", default=[], help="Allowed file/scope entry; repeatable")
    parser.add_argument("--read", action="append", default=[], help="Extra required context read; repeatable")
    parser.add_argument("--validation", default="<validation command>", help="Validation command")
    parser.add_argument("--worker-tool", default="<worker-tool>")
    parser.add_argument("--model", default="not exposed by tool")
    parser.add_argument("--provider-version", default="not exposed")
    parser.add_argument("--focus", default="mixed")
    parser.add_argument("--limitation", default="Task brief generated before worker execution.")
    parser.add_argument("--output", help="Output path; defaults to handoff/worker_tasks/YYYY-MM-DD_<name>.md")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output")
    args = parser.parse_args(argv)

    target = Path(args.target).resolve()
    name = slugify(args.name)
    output = Path(args.output) if args.output else target / "handoff" / "worker_tasks" / f"{date.today().isoformat()}_{name}.md"
    if not output.is_absolute():
        output = target / output
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file: {output}")
    template = (ROOT / "templates" / "worker-task.md").read_text(encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(template, args), encoding="utf-8", newline="\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
