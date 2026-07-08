# Multi-Project Memory Governance for AI Agents

A sanitized, open-source governance kit for running several AI-agent projects without turning one global memory store into a project database.

This repository distills patterns from multiple real agent-coordinated projects, with private paths, accounts, target names, credentials, run logs, and project-specific strategy removed. It is meant to be copied into your own repos and adapted.

## Core idea

```text
Global agent memory = compact cross-project signposts and user preferences.
Repo handoff = current engineering truth, validation state, worker outputs, gates.
Project notes / Obsidian = long-term strategy, rationale, decisions, reviews.
Skills = reusable procedures and judgment criteria, not project databases.
Session search = recall leads that must be verified before use.
```

## Why this exists

When one AI agent profile helps with several projects, durable memory can accidentally leak assumptions across domains. Examples:

- a creative/content preference biases a security workspace;
- a strict safety gate from a high-risk project over-constrains harmless local experiments;
- stale commit IDs, phase logs, or run artifacts remain in global memory;
- external workers assume they inherited context they never actually saw.

This kit provides a layered policy so future agents know where to read and where to write.

## Repository contents

- `docs/memory-governance-policy.md` — source-of-truth policy and routing matrix.
- `docs/handoff-index-policy.md` — how to keep `handoff/` useful instead of a dumping ground.
- `docs/agent-collaboration-policy.md` — coordinator/worker/reviewer contracts.
- `templates/` — copy-paste project files for `.hermes.md`, handoff governance, active queues, reviews, and worker tasks.
- `skills/note-taking/multi-project-memory-routing/SKILL.md` — a portable Hermes-style skill distilled from the policy.
- `scripts/check_public_safety.py` — simple scan for obvious private path/token patterns before publishing.

## Quick start

1. Copy `templates/handoff-memory-governance.md` into your project, usually as `handoff/memory_governance.md`.
2. Copy `templates/active-strategy-queue.md` into `handoff/active_strategy_queue.md`.
3. Add the required-read block from `templates/project-context-snippet.md` to `.hermes.md`, `AGENTS.md`, or `CLAUDE.md`.
4. If external workers are used, give them `templates/worker-task.md` and require explicit context reads.
5. Run:

```bash
python scripts/check_public_safety.py .
```

## Authority order

When layers disagree:

1. current explicit operator/user instruction;
2. live repo files, config, validation output, and current state;
3. repo handoff files for accepted engineering truth and safety gates;
4. project notes / Obsidian namespace for long-term rationale;
5. global durable agent memory for compact pointers and preferences;
6. session search only as recall, verified before use.

## Public-safety note

The examples intentionally use placeholders such as `<project-root>`, `<project-name>`, `<obsidian-project-namespace>`, and `<worker-tool>`. Do not replace them with private local paths, tokens, target details, raw scan output, account data, or client-sensitive evidence in a public fork.

## License

MIT. See `LICENSE`.
