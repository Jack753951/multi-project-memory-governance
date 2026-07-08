# Worker Task: Review handoff clarity

## Task

Review whether the project handoff files identify current truth and avoid relying on stale chat history.

## Required context reads

- `.hermes.md`
- `handoff/INDEX.md`
- `handoff/memory_governance.md`
- `handoff/active_strategy_queue.md`

## Allowed files/scope

- `handoff/`
- `.hermes.md`

## Disallowed actions

- Do not modify runtime configuration.
- Do not add private local paths, tokens, account data, or real project names.

## Expected output

Write a review artifact under `handoff/reviews/` with reviewer identity metadata and explicit limitations.

## Validation

Run `python scripts/mpmg.py validate-artifacts examples/agent-chaos-before-after/after` from the repository root.
