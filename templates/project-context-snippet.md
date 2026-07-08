# Project Context Snippet

Add this to `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, or equivalent.

## Required reads every session

1. `INDEX.md` or this project context file.
2. `handoff/memory_governance.md`.
3. `handoff/active_strategy_queue.md`.
4. `handoff/accepted_changes.md` for accepted changes relevant to the task.
5. `<project-notes-index>` if long-term strategy/rationale matters.

External workers must not assume access to global durable memory. If a fact matters for workers, write it into repo handoff, project context files, or the project notes namespace.

## Authority order

1. Current explicit user/operator instruction.
2. Live repo files and validation output.
3. Repo handoff files.
4. Project notes / Obsidian namespace.
5. Global durable memory as compact signposts only.
6. Session search as recall only.
