# Adoption Guide

This guide adds only as much authority governance as an existing repo needs. Start by mapping current tools; do not replace them or generate the full layout by default.

## 1. Inspect existing context systems

From this repository:

```bash
python scripts/mpmg.py integration-map /path/to/your/project
```

This is read-only. Review the detected instruction, specification, handoff, memory, and notes surfaces and answer the unresolved authority questions.

Optionally save one overlay file:

```bash
python scripts/mpmg.py integration-map /path/to/your/project --write
```

## 2. Choose the smallest adoption level

- Inspection only: keep no generated files.
- One-file overlay: review and commit `.mpmg/authority-map.md`.
- Selective contracts: add only missing worker-read, freshness, or notes-pointer rules.
- Full kit: initialize the complete layout only for projects that need it.

For full initialization:

```bash
python scripts/mpmg.py init --target /path/to/your/project --project-name MyProject --notes-namespace notes/Projects/MyProject
```

This creates the full handoff and notes structure:

- `handoff/memory_governance.md`
- `handoff/active_strategy_queue.md`
- `handoff/INDEX.md`
- `handoff/worker_tasks/README.md`
- `handoff/reviews/README.md`
- `notes/Projects/MyProject/00_Index.md`

## 3. Add the context snippet only where needed

Paste `templates/project-context-snippet.md` into `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, or the equivalent file used by your agent tools.

Do not paste the same rule into every tool blindly. Prefer the shared repo instruction surface already used by the project, and preserve directory/local scope.

## 4. Use bounded worker tasks

For any external worker, copy `templates/worker-task.md` and fill in required context reads, allowed files, disallowed actions, expected output, and validation.

## 5. Verify governance health

```bash
python scripts/validate_governance.py /path/to/your/project
python scripts/check_public_safety.py /path/to/your/project
```

The validator checks required handoff files, active queue gates, placeholders left in generated files, and required-read structure.

## 6. Review drift periodically

Use `docs/memory-governance-policy.md` as the review checklist. Confirm that global durable memory is compact, project-specific facts are in the project, and external workers have explicit context reads.

Also distinguish current observed state from intended behavior. A specification/implementation mismatch is drift to resolve, not a conflict that a generic precedence list can settle automatically.
