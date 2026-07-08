# Handoff Index Policy

`handoff/` is current collaboration memory, not the whole project database.

## Keep in `handoff/`

- `INDEX.md`: compact route map for future agents.
- `active_strategy_queue.md`: current lane, next safe actions, gates.
- `accepted_changes.md`: append/prepend-oriented audit log.
- worker task/result/review files for bounded tasks.
- current machine-readable state needed by local workflows.
- archive directories and migration manifests.

## Move out of `handoff/` when it grows

| Material | Better destination |
|---|---|
| Policies/contracts | `docs/policy/` |
| Strategy/reference planning | `docs/strategy/` or project notes |
| Domain objects/targets/assets | project-specific namespace such as `programs/<slug>/notes/` |
| Proof packets/evidence bundles | `labs/proofs/` or equivalent restricted area |
| Worker run receipts/usage JSON | `logs/runs/` |
| Old phase/review history | `handoff/archive/phase_history/` |
| Full pre-cleanup navigation snapshots | `handoff/archive/nav_snapshots/` |

## Required `handoff/INDEX.md` sections

```markdown
# Handoff Index

Status: active

## Read first
1. `<project-context-file>`
2. `handoff/current_navigation.md` or `handoff/active_strategy_queue.md`
3. `handoff/current_artifact_index.md` if present
4. `handoff/accepted_changes.md`

## Current machine state
- `<state-file>.json`

## Rolling worker IPC
- `<worker>_task.md`
- `<worker>_result.md`
- `<worker>_review.md`

## Moved out of handoff root
- Policies: `docs/policy/`
- Strategy/reference: `docs/strategy/`
- Logs/receipts: `logs/runs/`
- Archives: `handoff/archive/`
```

## Cleanup sequence

1. Inventory root files and classify by role.
2. Write a migration plan/manifest before moving files.
3. Archive full copies of long active navigation files before compacting.
4. Move files by category; do not move secrets or operator-owned authorization files automatically.
5. Update indexes and active pointers.
6. Patch only active references; avoid rewriting every archived artifact.
7. Run focused validation for scripts, JSON, schemas, and docs links.
8. Report cleanup as filesystem/documentation work only; it does not authorize external side effects.

## Policy hygiene rule

Do not create a new dated policy file for each correction to the same policy topic. Patch the active policy file and rely on git/history/archive for previous versions. Dated files are for events, checkpoints, evidence packets, and migration manifests.
