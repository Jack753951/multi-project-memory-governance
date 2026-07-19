# Quickstart

This path starts with a read-only overlay and adds the full kit only when needed.

## 1. Map an existing project

```bash
python scripts/mpmg.py integration-map /path/to/project
```

This writes nothing. It detects common instruction, specification, handoff, project-memory, and notes surfaces, then lists authority questions that still require a project owner.

To consume the result from another tool:

```bash
python scripts/mpmg.py integration-map /path/to/project --format json
```

## 2. Try the included contrast

```bash
python scripts/mpmg.py integration-map examples/agent-chaos-before-after/before
python scripts/mpmg.py integration-map examples/agent-chaos-before-after/after
python scripts/mpmg.py doctor examples/agent-chaos-before-after/before || true
python scripts/mpmg.py doctor examples/agent-chaos-before-after/after
```

The map inventories seams; the doctor applies the stricter full-kit checks. The first doctor command intentionally fails.

## 3. Save only one overlay if useful

```bash
python scripts/mpmg.py integration-map /path/to/project --write
```

This creates only `.mpmg/authority-map.md`. Review it before committing it. The generated status is `proposed-not-authoritative` because path detection cannot decide semantic truth.

## 4. Opt into the full kit only when needed

For a long-running or multi-agent project that needs handoff, notes, worker-task, and review contracts:

```bash
python scripts/mpmg.py init \
  --target /path/to/demo-project \
  --project-name DemoProject \
  --notes-namespace notes/Projects/DemoProject
```

Then validate it:

```bash
python scripts/mpmg.py audit /path/to/demo-project --format markdown
```

## 5. Add collaboration contracts selectively

```bash
python scripts/mpmg.py worker-task \
  --target /path/to/demo-project \
  --name review-routing \
  --task "Review memory routing and propose the next safe cleanup" \
  --scope handoff/ \
  --read notes/Projects/DemoProject/00_Index.md \
  --validation "python scripts/validate_governance.py ."
```

Use `plan-handoff-cleanup` only when a real handoff directory needs inventory. Its output is a plan, not an automatic move.
