# Active Strategy Queue — <project-name>

Status: active
Date: YYYY-MM-DD

## Long-term goal

<One paragraph describing the project goal.>

## Current phase

<Current phase and what is explicitly not authorized by this file.>

## Next safe actions

1. <Small, local, verifiable next action.>
2. <Next bounded review/implementation slice.>
3. <Update handoff/project notes after acceptance.>

## Active gates

- No scheduler/cron/webhook creation without explicit approval.
- No OAuth/token/credential mutation without explicit approval.
- No publishing/uploading/sending/external contact without explicit approval.
- No financial/trading/payment action without explicit approval.
- No live target-touching security work without explicit authorization and scope.
- No destructive deletion of user/runtime/generated data without explicit approval.

## Memory routing reminder

Project-specific state belongs here, in `handoff/accepted_changes.md`, named handoff artifacts, or `<project-notes-namespace>`. Global durable memory should contain only compact pointers and user-wide preferences.
