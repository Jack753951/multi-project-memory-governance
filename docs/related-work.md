# Related Work and Search Positioning

This project sits in an early, overlapping space: AI coding agent context hygiene, memory governance, handoff discipline, and repo-local authority boundaries.

The closest projects are not exact replacements. Most focus on one layer: memory storage, agent orchestration, handoff transport, AGENTS.md linting, or runtime policy. This repository focuses on the boundary between those layers: which context is allowed to be truth for a specific project, what external workers must read, what global memory must not store, what review artifacts must disclose, and how private agent workflows can be exported safely.

## Search phrases this project is meant to match

Use these phrases when describing, tagging, or comparing this repository:

- AI coding agent context hygiene
- AI agent project hygiene
- stop AI agents from mixing up projects
- AGENTS.md context rot
- Claude Code handoff governance
- Codex handoff governance
- repo-local memory governance
- AI agent memory boundary
- multi-agent handoff validation
- worker task brief validator
- AI review metadata
- public export safety for AI workflows
- authority boundary for AI coding agents
- long-running AI coding workflow hygiene

## Comparison table

| Category | Similar projects / search area | They usually focus on | This repository focuses on |
|---|---|---|---|
| Agent memory layers | MemMachine, ReMe, AGiXT, vector/database-backed memory systems | Storing, retrieving, refining, or sharing agent memory | Deciding what memory is allowed to mean in a specific project and keeping global memory out of project-state storage |
| Coding-agent handoff | ai-memory, claude-codex-handoff, loop/state-kernel projects | Passing state between Claude Code, Codex, Gemini CLI, or other coding agents | Bounded handoff with required reads, repo-local truth, worker scope limits, and review evidence |
| Context hygiene / AGENTS.md tools | agent-context-kit, context-guard, agents-lint, AGENTS.md/CLAUDE.md templates | Generating, linting, compacting, redacting, or refreshing agent context files | A full project hygiene layer across context files, handoff directories, worker tasks, review metadata, and public-export checks |
| Agent workflow governance | Tandem, agentic-os, SoloFlow, enterprise agent-control planes | Runtime policy, approvals, orchestration, action control, audit trails | Lightweight repo-local governance that can be used with existing agents without adopting a new runtime |
| Multi-agent collaboration | Traceplane, agent-room, workflow composers | Agent rooms, shared work threads, orchestration, collaboration UX | Filesystem-native project boundaries and evidence discipline that survive across tools and sessions |

## Differentiation

This project is not trying to be another agent runtime or universal memory backend. It is a small, inspectable governance kit for repositories where AI assistants already work.

It emphasizes:

1. **Authority boundaries** — chat history, session search, global memory, repo handoff, project notes, and live files have different authority.
2. **Multi-project isolation** — one agent profile should not turn into a shared project database.
3. **Worker context contracts** — external workers must have explicit required reads, scope limits, disallowed actions, expected output, and validation commands.
4. **Review artifact identity** — reviews should disclose route/tool, visible model when exposed, focus, and limitations.
5. **Public export safety** — private workflows should be transformed into sanitized public examples rather than copied raw.
6. **Doctor-first adoption** — a user should be able to run a command and see context drift before reading the full methodology.

## Honest positioning

This is an early-stage niche, but the underlying problem is growing. As more people use Claude Code, Codex, Cursor, Hermes, local subagents, AGENTS.md, CLAUDE.md, persistent memory, and multi-repo workflows, more projects will hit context drift and memory contamination.

The goal is to be discoverable by users who do not yet say "memory governance" but do say things like:

- "my AI agent keeps using rules from another repo";
- "my AGENTS.md is stale";
- "Claude and Codex need a handoff protocol";
- "my handoff folder is a mess";
- "external agents do not know what to read";
- "AI reviews need model/tool metadata";
- "I need to sanitize a private AI workflow before open-sourcing it".
