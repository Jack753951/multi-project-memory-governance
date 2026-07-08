# Field Guide from Multi-Project Practice

This guide summarizes the project lessons that shaped this kit. It is intentionally sanitized: it preserves reusable operating patterns, not private paths, accounts, targets, artifacts, or project history.

## Practice context

The patterns came from running AI agents across several different kinds of workspaces at once:

- software and infrastructure projects with repo-local validation;
- content/media automation with human-facing quality gates;
- security/lab workflows with strict authorization boundaries;
- research and investment-style workflows with current-fact freshness requirements;
- game/creative projects with setting/design truth separate from implementation handoff;
- helper/substrate repos that serve a larger main project.

The shared failure mode was not lack of memory. It was too much memory in the wrong layer.

## Lessons that survived sanitization

### 1. Global memory should be an index, not a database

Global durable memory is valuable when it points future sessions to the right project namespace, preference, or safety convention. It becomes harmful when it stores phase status, run artifacts, detailed strategy, or project-specific exceptions.

Use global memory for compact signposts such as:

```text
Project family X keeps engineering truth in repo handoff and long-term strategy in project notes.
```

Do not use it for:

```text
Task Y finished in commit Z; next run should use artifact A from local path B.
```

### 2. Handoff files need an index policy before they become a junk drawer

Every mature agent project eventually accumulates reviews, worker outputs, logs, receipts, queue notes, strategy fragments, and old phase summaries. Without an index policy, `handoff/` stops being handoff and becomes archaeological storage.

The practical fix is to keep a compact root index and move bulky or old artifacts into class-level directories such as `reviews/`, `worker_tasks/`, `archive/`, `evidence/`, or `unverified/`.

### 3. External workers do not inherit the coordinator's mind

Claude Code, Codex, local subagents, scheduled jobs, and scripts only know what their prompt includes and what they read from disk. A worker task must name required context reads explicitly. Otherwise the worker may optimize for local code while missing the project's long-term goal, current gates, or review standard.

### 4. Review identity matters

When multiple tools and models contribute reviews, every review artifact should state:

- route/tool;
- visible model or that the model was not exposed;
- provider/CLI version if visible;
- review focus;
- limitations.

This prevents future agents from treating a lightweight local check, a model review, a vision QA pass, and a production readiness review as equivalent.

### 5. Activation gates and learning loops must be separated

Some workflows need fast local iteration but strict external activation gates. Treat these differently:

- local-only drafts, tests, simulations, and learning loops can be batched and fast;
- upload, publication, OAuth, schedulers, target contact, payment, deletion, live scanning, trading, and destination changes require explicit gates.

Do not let strict activation gates freeze harmless learning, and do not let learning approval imply activation approval.

### 6. Obsidian/project notes are for rationale, not raw evidence dumps

Project notes are strongest when they preserve strategy, decisions, review synthesis, and navigable indexes. They are weakest when used as an unbounded dump of logs, secrets, raw scans, generated outputs, or per-run artifacts.

Use metadata fields such as `Status`, `Source`, `Date`, and `Repo truth` so notes can age safely.

### 7. Dedicated profiles help large projects, but do not replace routing

A dedicated agent profile reduces memory pollution for large projects. It does not remove the need for repo handoff, project notes, explicit worker reads, and activation gates.

Profile isolation is a containment strategy, not a memory architecture by itself.

### 8. Public export is a transformation, not a copy operation

A safe public version should extract process patterns and replace specifics with placeholders. It should not preserve exact local paths, private project names unless intended, raw logs, scan outputs, account details, credentials, run IDs, commits, or time-sensitive state.

The reusable artifact is the governance method, not the private project substrate.

## Reusable operating rules

1. Before saving memory, classify the fact by layer.
2. Before delegating to a worker, list required context reads.
3. Before accepting a worker output, verify it against files and commands.
4. Before archiving or deleting handoff material, update the root index.
5. Before publishing a sanitized repo, run a public-safety scan.
6. Before claiming project status, prefer live files and current handoff over session recall.
7. Before changing production-like behavior, require an explicit activation gate.

## Anti-patterns observed in practice

| Anti-pattern | Symptom | Replacement |
|---|---|---|
| Global-memory database | Future sessions inherit stale project state | Compact signpost + repo/project notes |
| Handoff junk drawer | Workers cannot find current truth | Root index + class directories |
| Invisible worker context | Worker misses strategy or gates | Required context reads |
| Review flattening | All reviews look equally authoritative | Reviewer identity block |
| Gate overloading | Local learning blocked by publication risk | Separate local loop from activation gate |
| Public copy-paste | Private facts leak into open source | Sanitized process extraction |

## What this repo intentionally does not include

- private project paths;
- user account details;
- credentials, cookies, tokens, or keys;
- raw logs or scan output;
- project-specific vulnerability, financial, business, or creative strategy;
- commit IDs, issue IDs, run IDs, phase-completion logs, or scheduler state.
