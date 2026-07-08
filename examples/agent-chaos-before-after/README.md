# Agent Chaos Before/After Demo

This example is for people who feel the pain before they know the phrase "memory governance".

It shows a messy long-running AI-agent project before and after adding project memory boundaries, handoff navigation, bounded worker tasks, and review metadata.

## Try it

The `before/` project is intentionally unhealthy:

```bash
python ../../scripts/mpmg.py doctor before
python ../../scripts/mpmg.py plan-handoff-cleanup before --format markdown
```

The `after/` project is the same synthetic project after applying the kit:

```bash
python ../../scripts/mpmg.py doctor after
python ../../scripts/mpmg.py validate-artifacts after
```

Expected shape:

- `before/` fails governance validation and has no explicit worker/review artifact metadata.
- `after/` passes layout checks, keeps handoff files navigable, and labels worker/review boundaries.

All names and content are synthetic.
