# Adoption Guide

This guide turns an existing repo into a memory-governed AI-agent workspace.

## 1. Initialize governance files

From this repository:

```bash
python scripts/init_governance.py --target /path/to/your/project --project-name MyProject --notes-namespace notes/Projects/MyProject
```

This creates:

- `handoff/memory_governance.md`
- `handoff/active_strategy_queue.md`
- `handoff/INDEX.md`
- `handoff/worker_tasks/README.md`
- `handoff/reviews/README.md`
- `notes/Projects/MyProject/00_Index.md`

## 2. Add the context snippet

Paste `templates/project-context-snippet.md` into `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, or the equivalent file used by your agent tools.

## 3. Use bounded worker tasks

For any external worker, copy `templates/worker-task.md` and fill in required context reads, allowed files, disallowed actions, expected output, and validation.

## 4. Verify governance health

```bash
python scripts/validate_governance.py /path/to/your/project
python scripts/check_public_safety.py /path/to/your/project
```

The validator checks required handoff files, active queue gates, placeholders left in generated files, and required-read structure.

## 5. Review drift periodically

Use `docs/memory-governance-policy.md` as the review checklist. Confirm that global durable memory is compact, project-specific facts are in the project, and external workers have explicit context reads.
