# Project Context Snippet

Add this to `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, or equivalent.

## Required reads every session

1. `INDEX.md` or this project context file.
2. `handoff/memory_governance.md`.
3. `handoff/active_strategy_queue.md`.
4. `handoff/accepted_changes.md` for accepted changes relevant to the task.
5. `<project-notes-index>` if long-term strategy/rationale matters.

External workers must not assume access to global durable memory. If a fact matters for workers, write it into repo handoff, project context files, or the project notes namespace.

## Authority order by question

1. **Task and scope:** current explicit user/operator instruction.
2. **Current observed state:** live repo files, configuration, and fresh validation evidence.
3. **Intended behavior:** current accepted requirements, specifications, and policies.
4. **Accepted work state:** verified repo handoff.
5. **Long-term rationale:** project notes / Obsidian namespace.
6. **Recall and discovery:** compact global-memory signposts, then session search; verify changing facts.

Current instruction controls the task but does not rewrite observed facts. Expose specification/implementation drift for resolution.
