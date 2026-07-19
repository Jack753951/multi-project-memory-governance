# Stop AI Agents from Mixing Up Your Projects

[![CI](https://github.com/Jack753951/multi-project-memory-governance/actions/workflows/ci.yml/badge.svg)](https://github.com/Jack753951/multi-project-memory-governance/actions/workflows/ci.yml)

AI coding agents do not only need more memory. They need a reliable way to decide **what to trust**.

An agent may have live files, old chat history, global memory, project notes, handoff documents, and instructions from another worker available at the same time. The hard problem is not storing all of it. The hard problem is deciding:

- where each kind of knowledge belongs;
- which source wins when two sources disagree;
- when remembered information must be checked against live state;
- what an external worker must read instead of assuming it inherited context.

Multi-Project Memory Governance (MPMG) is a small, filesystem-native method and toolkit for defining those authority boundaries in long-running AI-assisted projects.

> **Core rule:** every important fact should have one authoritative home. Lower-authority memory may help an agent find context, but it must not silently override current instructions, live files, or verified project state.

This prevents concrete failures such as:

- an agent applying rules or phase state from another repository;
- stale chat history overruling current code and validation output;
- global memory becoming an outdated project database;
- a Claude Code, Codex, Cursor, Hermes, or local worker acting without the project context it was expected to read;
- handoff and review artifacts losing their source, validation, or limitation metadata.

This is not a memory database, agent runtime, or replacement for `AGENTS.md` / `CLAUDE.md`. It is a governance layer for the context systems you already use: repo files, handoff documents, project notes or Obsidian, durable agent memory, skills, and session history.

## Try the boundary checks

Run the read-only doctor first:

```bash
python scripts/mpmg.py doctor /path/to/your/project
```

Then inspect a concrete before/after demo:

```bash
python scripts/mpmg.py doctor examples/agent-chaos-before-after/before || true
python scripts/mpmg.py doctor examples/agent-chaos-before-after/after
python scripts/mpmg.py validate-artifacts examples/agent-chaos-before-after/after
```

See `docs/before-after-demo.md` for the walkthrough.

## Core model: which source wins?

```text
Higher authority

1. Current user / operator instruction
2. Live repo files, configuration, and current validation output
3. Verified repo handoff: accepted changes, active queue, and gates
4. Project notes / Obsidian: long-term rationale and decisions
5. Global agent memory: compact cross-project signposts and preferences
6. Session search: recall leads that must be verified

Lower authority
```

Higher-authority sources win when layers conflict. Skills sit beside this order: they describe reusable procedures, but do not store current project truth.

The layers are separated to limit stale or cross-project information from gaining decision authority—not merely to organize files.

See `docs/architecture.md` for the diagram and layer contract.

## What is included

- `docs/memory-governance-policy.md` — source-of-truth policy and routing matrix.
- `docs/handoff-index-policy.md` — how to keep `handoff/` useful instead of a dumping ground.
- `docs/agent-collaboration-policy.md` — coordinator/worker/reviewer contracts.
- `docs/quickstart.md` — five-minute guided path.
- `docs/before-after-demo.md` — concrete messy-project demo for the core pain point.
- `docs/related-work.md` — similar GitHub project categories, search phrases, and differentiation.
- `docs/adoption-matrix.md` — choose the right governance weight for each project type.
- `docs/adoption-guide.md` — step-by-step adoption guide.
- `docs/release-checklist.md` — release verification checklist.
- `docs/field-guide-from-practice.md` — sanitized summary of project lessons that shaped the kit.
- `docs/tooling.md` — command reference for the included tools.
- `templates/` — copy-paste project files for context, handoff governance, active queues, reviews, and worker tasks.
- `examples/minimal-project/` — synthetic governed project layout.
- `examples/agent-chaos-before-after/` — messy-to-governed demo that shows the pain quickly.
- `examples/multi-agent-review/` — synthetic coordinator/worker/reviewer handoff flow.
- `examples/public-export/` — synthetic sanitized export workflow.
- `skills/note-taking/multi-project-memory-routing/SKILL.md` — portable Hermes-style skill.
- `scripts/mpmg.py` — unified CLI for init, validate, audit, doctor, worker-task, export, and cleanup planning.
- `scripts/init_governance.py` — bootstrap governance files into a repo.
- `scripts/validate_governance.py` — validate a governed project layout.
- `scripts/check_public_safety.py` — scan for obvious private path/token patterns before publishing.
- `scripts/governance_audit.py` — one-command validate + public-safety audit.
- `scripts/new_worker_task.py` — generate bounded worker task briefs.
- `scripts/export_public_subset.py` — produce a sanitized public subset export.
- `scripts/doctor.py` — check local environment and governance health.
- `scripts/plan_handoff_cleanup.py` — inventory `handoff/` and suggest cleanup destinations without moving files.
- `scripts/validate_artifacts.py` — validate worker task and review artifact metadata.
- `ROADMAP.md` and `CHANGELOG.md` — project direction and release history.
- `.github/workflows/ci.yml` — CI for tests, example validation, and public safety scan.

## Quick start

Clone this repo, then initialize governance in another project:

```bash
python scripts/mpmg.py init \
  --target /path/to/your/project \
  --project-name MyProject \
  --notes-namespace notes/Projects/MyProject
```

If the context file does not exist, the initializer creates `.hermes.md`. If your project already has `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, or another agent context file, merge `templates/project-context-snippet.md` into the existing file.

Validate:

```bash
python scripts/mpmg.py validate /path/to/your/project
python scripts/mpmg.py safety-scan /path/to/your/project
python scripts/mpmg.py audit /path/to/your/project --format markdown
python scripts/mpmg.py doctor /path/to/your/project
```

Try the included example:

```bash
python scripts/validate_governance.py examples/minimal-project
python -m unittest discover -s tests
```

## Authority order

When layers disagree:

1. current explicit operator/user instruction;
2. live repo files, config, validation output, and current state;
3. repo handoff files for accepted engineering truth and safety gates;
4. project notes / Obsidian namespace for long-term rationale;
5. global durable agent memory for compact pointers and preferences;
6. session search only as recall, verified before use.

## Who should use this

Use it if you:

- run one AI assistant profile across multiple repos;
- use external coding/review agents that need explicit context boundaries;
- maintain Obsidian or Markdown project notes alongside code;
- want repo-local handoff files to stay readable;
- need a safe public-export discipline for private agent workflows.

Do not use it as a substitute for secrets management, legal/compliance review, or domain-specific safety policy.

## Related work and search positioning

This project overlaps with agent memory layers, Claude/Codex handoff tools, AGENTS.md/context hygiene tools, agent workflow governance, and multi-agent collaboration systems. Its differentiator is the repo-local boundary between those layers: which context is truth, what global memory must not store, what workers must read, what review artifacts must disclose, and how private AI-agent workflows are safely exported.

See `docs/related-work.md` for the detailed comparison and keyword map.

## Public-safety note

The examples intentionally use placeholders such as `<project-root>`, `<project-name>`, `<project-notes-namespace>`, and `<worker-tool>`. Do not replace them with private local paths, tokens, target details, raw scan output, account data, or client-sensitive evidence in a public fork.

## Development

```bash
python -m unittest discover -s tests
python scripts/validate_governance.py examples/minimal-project
python scripts/check_public_safety.py .
```

## License

MIT. See `LICENSE`.
