# Worker Task: <short-name>

## Task

<What to accomplish.>

## Required context reads

- `<project-context-file>`
- `handoff/memory_governance.md`
- `handoff/active_strategy_queue.md`
- `<specific artifact for this task>`

## Allowed files/scope

- `<path>`

## Disallowed actions

- Do not edit secrets, credentials, production config, scheduler/OAuth settings, or unrelated files.
- Do not publish, upload, send, contact external parties, trade, pay, scan live targets, or delete user data.

## Expected output

Write result to `handoff/reviews/<date>_<short-name>.md` or another named artifact.

## Validation

Run:

```bash
<validation command>
```

## Required review identity block

```markdown
## Reviewer identity

- Reviewer route/tool: <worker-tool>
- Visible runtime model: <model if exposed, else not exposed by tool>
- Provider / CLI version if visible: <value or not exposed>
- Review focus: <engineering | strategy | safety | UX | mixed>
- Limitation: <what was not inspected or unavailable>
```
