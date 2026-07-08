# Adoption Matrix

Use this matrix to choose how much of the kit to adopt. The goal is not to make every project heavy; it is to match governance weight to collaboration risk.

| Project shape | Minimum adoption | Recommended tools | Why |
|---|---|---|---|
| Solo experiment | `.hermes.md`, `handoff/INDEX.md` | `mpmg init`, `mpmg validate` | Enough context to resume without turning memory into a log. |
| Multi-agent coding project | handoff policy, active queue, worker tasks, reviews | `mpmg worker-task`, `mpmg validate-artifacts`, `mpmg doctor` | External workers need explicit reads and bounded output. |
| Project with Obsidian/project notes | repo handoff plus notes index pointer | `mpmg audit`, `mpmg doctor` | Keeps strategy/rationale discoverable without copying it into global memory. |
| Public export candidate | sanitized docs/templates/examples only | `mpmg export-public`, `mpmg safety-scan` | Export should transform process patterns, not private state. |
| Messy long-running project | handoff cleanup plan before migration | `mpmg plan-handoff-cleanup` | Inventory first; avoid destructive cleanup. |
| Sensitive project | local authorization/safety gates, no private details in global memory | `mpmg audit`, project-specific review | Generic checks help but do not replace domain safety review. |

## Recommended default for new projects

Start with:

```bash
python scripts/mpmg.py init --target /path/to/project --project-name MyProject --notes-namespace notes/Projects/MyProject
python scripts/mpmg.py doctor /path/to/project
```

Add worker/review artifacts only when more than one agent or reviewer is involved.
