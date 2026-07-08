# Worker Task: review-routing

## Task

Review whether the synthetic project keeps memory, handoff, and review responsibilities separated.

## Required context reads

- `.hermes.md`
- `handoff/memory_governance.md`
- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`

## Allowed files/scope

- `handoff/`

## Disallowed actions

- Do not edit secrets, credentials, production config, scheduler/OAuth settings, or unrelated files.
- Do not publish, upload, send, contact external parties, trade, pay, scan live targets, or delete user data.

## Expected output

Write result to `handoff/reviews/2026-01-01_review-routing.md`.

## Validation

Run:

```bash
python scripts/validate_governance.py examples/multi-agent-review
```

## Required review identity block

```markdown
## Reviewer identity

- Reviewer route/tool: synthetic-worker
- Visible runtime model: not exposed by tool
- Provider / CLI version if visible: not exposed
- Review focus: governance
- Limitation: synthetic example only
```
