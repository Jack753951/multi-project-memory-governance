# Active Strategy Queue — MultiAgentExample

Status: active
Date: 2026-01-01

## Long-term goal

Demonstrate a minimal governed AI-agent project layout.

## Current phase

Template demonstration only; no external side effects are authorized.

## Next safe actions

1. Run the governance validator.
2. Create a synthetic worker task if needed.
3. Record accepted template changes in handoff.

## Active gates

- No scheduler/cron/webhook creation without explicit approval.
- No OAuth/token/credential mutation without explicit approval.
- No publishing/uploading/sending/external contact without explicit approval.
- No financial/trading/payment action without explicit approval.
- No live target-touching security work without explicit authorization and scope.
- No destructive deletion of user/runtime/generated data without explicit approval.

## Memory routing reminder

Project-specific state belongs here, in `handoff/accepted_changes.md`, named handoff artifacts, or `notes/Projects/MultiAgentExample/`. Global durable memory should contain only compact pointers and user-wide preferences.
