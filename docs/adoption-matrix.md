# Adoption Matrix

Use this matrix to choose how much of the kit to adopt. The goal is not to make every project heavy; it is to match governance weight to collaboration risk.

| Project shape | Minimum adoption | Recommended tools | Why |
|---|---|---|---|
| Existing project using AGENTS.md, Claude, Cline, Sopify, or specs | read-only integration map | `mpmg integration-map` | Find seams before adding another context system. |
| Solo experiment | inspect only, or one `.mpmg/authority-map.md` if a real conflict exists | `mpmg integration-map` | Avoid turning a small project into a governance exercise. |
| Multi-agent coding project | handoff policy, active queue, worker tasks, reviews | `mpmg worker-task`, `mpmg validate-artifacts`, `mpmg doctor` | External workers need explicit reads and bounded output. |
| Project with Obsidian/project notes | repo handoff plus notes index pointer | `mpmg audit`, `mpmg doctor` | Keeps strategy/rationale discoverable without copying it into global memory. |
| Public export candidate | sanitized docs/templates/examples only | `mpmg export-public`, `mpmg safety-scan` | Export should transform process patterns, not private state. |
| Messy long-running project | handoff cleanup plan before migration | `mpmg plan-handoff-cleanup` | Inventory first; avoid destructive cleanup. |
| Sensitive project | local authorization/safety gates, no private details in global memory | `mpmg audit`, project-specific review | Generic checks help but do not replace domain safety review. |

## Recommended default

Start read-only:

```bash
python scripts/mpmg.py integration-map /path/to/project
```

Save the one-file overlay only if it clarifies a real seam. Use `mpmg init` and add worker/review artifacts only when a long-running or multi-agent project needs the full contract.
