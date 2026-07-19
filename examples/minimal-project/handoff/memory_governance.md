# Project Memory Governance

Status: active
Scope: `ExampleProject`, repo-local handoff, project notes, external worker prompts, and session recall.

## Authority order by question

1. **Task and scope:** current explicit user/operator instruction.
2. **Current observed state:** live repo files, configuration, and fresh validation evidence.
3. **Intended behavior:** current accepted requirements, specifications, and policies.
4. **Accepted work state:** verified repo handoff.
5. **Long-term rationale:** project notes.
6. **Recall and discovery:** compact global-memory signposts, then session search; verify changing facts before acting.

Current instruction controls the task but does not rewrite observed facts. Specification/implementation disagreement is drift to resolve.

## Where information belongs

| Item type | Destination |
|---|---|
| User-wide stable preference | Global durable memory, compact declarative fact |
| Project engineering result | `handoff/accepted_changes.md` plus relevant artifact |
| Current priority/next safe action | `handoff/active_strategy_queue.md` |
| Worker task/result/review | `handoff/worker_tasks/`, `handoff/reviews/`, then accepted summary |
| Long-term strategy/rationale/decision | `notes/Projects/ExampleProject/` |
| Reusable workflow | Skill or shared governance doc |
| Temporary run output | Current session or dated handoff artifact if needed |
| Secret/credential/token/private data | Store nowhere; record only safe handling rule |

## Bridge-file rule

External workers do not inherit global durable memory. If a fact matters for workers, write it into one of:

- `.hermes.md`
- `AGENTS.md` / `CLAUDE.md` or equivalent
- `handoff/active_strategy_queue.md`
- `handoff/memory_governance.md`
- `notes/Projects/ExampleProject/00_Index.md`

## Memory-save checklist

Before saving durable global memory:

1. Is it stable for weeks/months?
2. Is it cross-project/profile-level rather than project implementation state?
3. Is it non-secret and non-sensitive?
4. Can it be expressed as one compact declarative signpost?
5. If project-specific, has it been written to handoff/notes instead?
