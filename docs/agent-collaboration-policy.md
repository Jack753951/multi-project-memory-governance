# Agent Collaboration Policy

Use this when a coordinator agent works with external workers such as coding agents, reviewers, local scripts, or CLI assistants.

## Core principle

External workers do not automatically inherit the coordinator's durable memory, chat context, or full project note vault.

A typical worker prompt is only:

```text
project context file + bounded task file + optional safety footer/tool limits
```

Filesystem access means a worker can read files if instructed; it does not mean it has already read them.

## Role split

| Role | Default responsibility |
|---|---|
| Human/operator | goals, authorization, risk tolerance, approvals |
| Coordinator/verifier | classify risk, route work, verify outputs, update handoff |
| Implementation worker | bounded edits to code/docs/templates |
| Strategy/process reviewer | challenge assumptions, fit, risk, and governance |
| QA/safety reviewer | validate correctness, gates, memory routing, and handoff clarity |
| Local scripts | deterministic validation, linting, schema checks, safety scans |

## Worker task contract

Every non-trivial worker task should include:

- Task
- Required context reads
- Allowed files/scope
- Disallowed actions
- Expected output shape
- Validation command
- Where to write result
- Safety constraints

## Review contract

Reviews should include:

```markdown
## Reviewer identity

- Reviewer route/tool: <coordinator | subagent | CLI | local script | other>
- Visible runtime model: <model if exposed, else not exposed by tool>
- Provider / CLI version if visible: <value or not exposed>
- Review focus: <engineering | strategy | safety | UX | mixed>
- Limitation: <what was not inspected or unavailable>
```

Also include:

- context read attestation;
- scope inspected;
- validation run and output summary;
- verdict: `PASS`, `CONCERN`, `BLOCKED`, or `REJECT`;
- risks and next safe action.

## Acceptance flow

1. Coordinator creates proposal/task.
2. Worker completes bounded work or review.
3. Coordinator inspects files and runs validation.
4. Coordinator records accepted result in `handoff/accepted_changes.md`.
5. Coordinator updates `handoff/active_strategy_queue.md` if priorities changed.
6. Durable rationale goes to project notes / Obsidian if it should guide future reasoning.

## Hard boundaries

Workers may not independently approve or perform:

- scheduler/cron/webhook creation or mutation;
- OAuth/token/credential changes;
- publishing/uploading/sending/contacting external parties;
- financial/trading/payment actions;
- live target-touching security actions;
- destructive deletion of user/runtime/generated data;
- global profile memory edits that store project state.

## Required context reads pattern

Use a compact block rather than dumping an entire vault:

```text
Before editing or reviewing, read:
- <project-context-file>
- handoff/memory_governance.md
- handoff/active_strategy_queue.md
- handoff/accepted_changes.md or named artifact for this slice
- <project-notes-index> if long-term rationale matters
```
