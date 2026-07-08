# Multi-Agent Review Example

This synthetic example shows how to brief an external worker without assuming it inherits global memory or private chat context.

## Flow

1. Coordinator reads project context, handoff, and notes index.
2. Coordinator generates `handoff/worker_tasks/2026-01-01_review-routing.md`.
3. Worker reads only the required files named in the brief.
4. Worker writes a review artifact with a reviewer identity block.
5. Coordinator verifies the result and updates accepted changes only if the result is accepted.

## Files

- `.hermes.md` — short agent context and authority order.
- `handoff/worker_tasks/2026-01-01_review-routing.md` — bounded worker task.
- `handoff/reviews/2026-01-01_review-routing.md` — synthetic review output.
- `handoff/accepted_changes.md` — where accepted outcomes would be recorded.

This example contains no private project data.
