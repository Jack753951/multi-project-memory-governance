# Tooling

This repository includes small Python tools that make the governance policy usable instead of merely descriptive.

## `scripts/init_governance.py`

Bootstrap a target project with handoff, notes, and agent-context files.

```bash
python scripts/init_governance.py   --target /path/to/project   --project-name MyProject   --notes-namespace notes/Projects/MyProject
```

Use `--force` to overwrite generated files.

## `scripts/validate_governance.py`

Check that a project has required governance files and basic content sections.

```bash
python scripts/validate_governance.py /path/to/project
```

## `scripts/check_public_safety.py`

Scan text files for obvious private paths and common token patterns before public export.

```bash
python scripts/check_public_safety.py /path/to/project-or-export
```

This is not a complete secret scanner. Treat it as a lightweight preflight check.

## `scripts/governance_audit.py`

Run validation plus public-safety scan and produce a concise audit report.

```bash
python scripts/governance_audit.py /path/to/project --format markdown
python scripts/governance_audit.py /path/to/project --format json
```

Use this before handoff cleanup, public export, or onboarding a new agent profile.

## `scripts/new_worker_task.py`

Generate a bounded worker task from `templates/worker-task.md`.

```bash
python scripts/new_worker_task.py   --target /path/to/project   --name review-memory-routing   --task "Review handoff routing and propose a cleanup plan"   --scope "handoff/ docs/"   --validation "python scripts/validate_governance.py ."
```

The generated task lands in `handoff/worker_tasks/YYYY-MM-DD_<name>.md` by default.

## `scripts/export_public_subset.py`

Copy docs/templates/skills/scripts/examples into a sanitized export directory and run the public safety scan.

```bash
python scripts/export_public_subset.py --output /tmp/memory-governance-export
```

Use this when adapting a private governance substrate into a public teaching repo.


## Unified CLI

All helpers are also available through one command:

```bash
python scripts/mpmg.py init --target /path/to/project --project-name MyProject --notes-namespace notes/Projects/MyProject
python scripts/mpmg.py validate /path/to/project
python scripts/mpmg.py audit /path/to/project --format markdown
python scripts/mpmg.py doctor /path/to/project
python scripts/mpmg.py validate-artifacts /path/to/project
python scripts/mpmg.py worker-task --target /path/to/project --name review-routing --task "Review routing" --scope handoff/
python scripts/mpmg.py plan-handoff-cleanup /path/to/project --format markdown
python scripts/mpmg.py export-public --output /tmp/mpmg-export --force
```

## `scripts/doctor.py`

Check Python, git availability, governance validation, public safety, common handoff directories, and worker/review artifact metadata. Use this as the first diagnostic command when an AI-agent project starts to feel context-drifted.

## `scripts/plan_handoff_cleanup.py`

Inventory a handoff directory and suggest destinations. It does not move files; use it to create a human-reviewed cleanup plan.

## `scripts/validate_artifacts.py`

Validate that worker task briefs include task, required reads, scope, disallowed actions, expected output, and validation sections; validate that review artifacts include reviewer identity metadata.
