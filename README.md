# Multi-Project Memory Governance

[![CI](https://github.com/Jack753951/multi-project-memory-governance/actions/workflows/ci.yml/badge.svg)](https://github.com/Jack753951/multi-project-memory-governance/actions/workflows/ci.yml)

AI coding agents do not only need more memory. They need a reliable way to decide **what to trust**.

An agent may have live files, old chat history, global memory, project notes, handoff documents, and instructions from another worker available at the same time. The hard problem is not storing all of it. The hard problem is deciding:

- where each kind of knowledge belongs;
- which source answers each kind of question when sources disagree;
- when remembered information must be checked against live state;
- what an external worker must read instead of assuming it inherited context.

Multi-Project Memory Governance (MPMG) is a small, filesystem-native **authority overlay** for long-running AI-assisted projects. It sits between the context systems you already use and makes their seams explicit.

> **Core rule:** every important question should have a named authority. Task scope, observed state, intended behavior, accepted work state, and long-term rationale may legitimately have different owners.

This helps expose and reduce failures such as:

- an agent applying rules or phase state from another repository;
- stale chat history overruling current code and validation output;
- global memory becoming an outdated project database;
- a Claude Code, Codex, Cursor, Hermes, or local worker acting without the project context it was expected to read;
- handoff and review artifacts losing their source, validation, or limitation metadata.

This is not a memory database, agent runtime, or replacement for `AGENTS.md`, `CLAUDE.md`, Cline Memory Bank, Sopify, Spec Kit, OpenSpec, Ruler, or runtime policy. Those tools keep their jobs. The default thin-overlay path only maps which system owns which question, where freshness must be checked, and what an external worker must read. Optional full-kit commands can add a handoff and validation layout when a project explicitly needs one.

## Start with the thin overlay

Inspect an existing project without changing it:

```bash
python scripts/mpmg.py integration-map /path/to/your/project
```

Or run it directly from GitHub without cloning:

```bash
uvx --from git+https://github.com/Jack753951/multi-project-memory-governance.git mpmg integration-map /path/to/your/project
```

The command detects common repository-local instruction, specification, handoff, project-memory, and notes surfaces. It proposes roles and unresolved questions; it does not claim to infer semantic truth.

To save one reviewable overlay without modifying existing tool files:

```bash
python scripts/mpmg.py integration-map /path/to/your/project --write
# writes only /path/to/your/project/.mpmg/authority-map.md
```

Use the larger doctor and governance layout only if the project needs them:

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

## Core model: what kind of truth is being asked for?

| Question | Primary authority |
|---|---|
| What should the agent do now? | Current explicit user/operator instruction for task and scope |
| What is happening now? | Direct observation of the relevant system of record and fresh question-matched evidence; repo files establish checkout state, not deployment state |
| What should the system do? | Current accepted requirements, specifications, and policies |
| What work state was accepted? | Verified repo handoff, active queue, decisions, and evidence |
| Why was a durable decision made? | Project notes or decision records |
| Where should a future session look? | Compact global-memory signposts |
| What might an old conversation contain? | Session search as a recall lead that must be verified |

Current instruction controls the task; it does not rewrite observed facts. A specification/implementation mismatch is drift to resolve rather than a reason to silently discard either side. Skills sit beside these authorities: they describe reusable procedures, but do not store current project truth.

The layers are separated to limit stale or cross-project information from gaining decision authority—not merely to organize files.

See `docs/architecture.md` for the layer contract and `docs/thin-authority-overlay.md` for integration guidance.

## What is included

- `docs/memory-governance-policy.md` — source-of-truth policy and routing matrix.
- `docs/handoff-index-policy.md` — how to keep `handoff/` useful instead of a dumping ground.
- `docs/agent-collaboration-policy.md` — coordinator/worker/reviewer contracts.
- `docs/quickstart.md` — five-minute guided path.
- `docs/before-after-demo.md` — concrete messy-project demo for the core pain point.
- `docs/related-work.md` — mature adjacent tools, their responsibilities, and integration boundaries.
- `docs/adoption-matrix.md` — choose the right governance weight for each project type.
- `docs/adoption-guide.md` — step-by-step adoption guide.
- `docs/thin-authority-overlay.md` — read-only inventory, one-file overlay, and integration roles for existing tools.
- `docs/release-checklist.md` — release verification checklist.
- `docs/field-guide-from-practice.md` — sanitized summary of project lessons that shaped the kit.
- `docs/tooling.md` — command reference for the included tools.
- `templates/` — copy-paste project files for context, handoff governance, active queues, reviews, and worker tasks.
- `examples/minimal-project/` — synthetic governed project layout.
- `examples/agent-chaos-before-after/` — messy-to-governed demo that shows the pain quickly.
- `examples/multi-agent-review/` — synthetic coordinator/worker/reviewer handoff flow.
- `examples/public-export/` — synthetic sanitized export workflow.
- `skills/note-taking/multi-project-memory-routing/SKILL.md` — portable Hermes-style skill.
- `scripts/mpmg.py` — unified CLI for read-only integration mapping, optional full initialization, validation, audit, worker tasks, export, and cleanup planning.
- `scripts/integration_map.py` — detect existing context surfaces and generate a non-authoritative integration map.
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

Clone this repo, then inspect another project read-only:

```bash
python scripts/mpmg.py integration-map /path/to/your/project
```

If one authority map is enough, save it with `--write`. If the project needs the complete handoff and notes structure, opt into full initialization:

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

## Conflict rule

First classify the question. Current instruction owns task and scope; fresh evidence owns observed state; accepted requirements/specifications/policies own intended behavior. Verified handoff, notes, global memory, and session history provide progressively less current context. If two primary authorities disagree, expose the conflict, name an owner, and verify what must change instead of silently flattening every case into one list.

## Who should use this

Use it if you:

- run one AI assistant profile across multiple repos;
- use external coding/review agents that need explicit context boundaries;
- maintain Obsidian or Markdown project notes alongside code;
- want repo-local handoff files to stay readable;
- need a safe public-export discipline for private agent workflows.

Do not use it as a substitute for secrets management, legal/compliance review, or domain-specific safety policy.

## Related work and scope

This project complements agent memory layers, Claude/Codex handoff tools, AGENTS.md/context tools, specification workflows, and agent governance runtimes. Its narrow role is the boundary between those systems: which context owns which question, what global memory must not store, what workers must read, and where conflicts require human resolution.

See `docs/related-work.md` for the detailed comparison and integration boundaries.

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
