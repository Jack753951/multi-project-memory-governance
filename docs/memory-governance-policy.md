# Memory Governance Policy

Status: public template
Scope: multi-project AI-agent workspaces, Hermes-like agents, external coding agents, repo-local handoff files, and project note systems such as Obsidian.

## Purpose

This policy prevents project state from leaking into global agent memory while preserving enough context for future agents and external workers to collaborate safely.

## Layer responsibilities

| Layer | Use for | Do not use for |
|---|---|---|
| Global durable memory | Stable user-wide preferences, cross-project safety/routing principles, compact pointers to project namespaces | Progress logs, PR/issue/commit IDs, phase completion, run artifacts, full strategy docs, secrets |
| Project context files | Project constitution, required reads, role split, hard gates | Long histories or rolling worker outputs |
| Repo handoff | Accepted changes, validation outcomes, worker tasks/results, active queue, current safety gates | Whole project database, raw caches, private secrets, stale duplicate policies |
| Active strategy queue | Current lane, next safe slices, deferred lanes, approval-locked work | Full history or detailed strategy archive |
| Project notes / Obsidian | Long-term rationale, research, decisions, experiments, review synthesis | Raw credentials, private evidence, tokens, sensitive target data |
| Skills | Reusable procedure and judgment criteria | Project logs, project-specific current state |
| Session search | Recall leads from prior conversations | Final authority without file verification |

## Authority order

1. Current explicit user/operator instruction.
2. Live project files, config, validation output, and current repo state.
3. Repo handoff files for engineering truth and gates.
4. Project notes / Obsidian namespace for strategy, rationale, decisions, and reviews.
5. Global durable memory for compact preferences and pointers.
6. Session search as recall only; verify before relying on it.

## Memory-save checklist

Before writing durable global memory, ask:

1. Is it stable for weeks/months?
2. Is it cross-project/profile-level rather than one repo's current implementation state?
3. Is it non-secret and non-sensitive?
4. Can it be written as one compact declarative fact?
5. If project-specific, has it already been written into repo handoff or project notes instead?

Prefer declarative memory:

```text
Project X uses repo handoff as engineering truth and project notes for long-term rationale.
```

Avoid imperative memory:

```text
Always run command Y before doing anything.
```

Imperative durable memory can accidentally override future project-specific instructions.

## Project note metadata

Use this for durable project notes:

```markdown
Status: active | superseded | rejected | experiment | reference
Source: User | Coordinator | Worker | Reviewer | Mixed
Date: YYYY-MM-DD
Repo truth: <relative/path/to/handoff-or-code-file>
```

Each project should maintain an index note that links only to current/active guidance. Mark old notes `superseded`, `rejected`, or `reference`; do not silently delete historical rationale.

## Sensitive project rule

For cybersecurity, finance, legal, health, client, or private-account projects, do not store these in global memory or broad public notes:

- secrets, API keys, OAuth tokens, cookies, credentials;
- raw scan outputs, target details, exploit payloads, loot, hashes;
- private scope/rules, client-sensitive evidence, financial account data;
- one-off validation transcripts or stale run IDs.

Store only the handling rule, methodology, or non-sensitive decision rationale.

## Drift checks for periodic reviews

Periodic reviews should explicitly check:

- memory drift: did global memory over- or under-state project truth?
- handoff drift: do accepted changes, named artifacts, active queue, and live files agree?
- goal drift: is the project still pursuing its stated success metric?
- structure drift: are files accumulating without a compact current index?
- safety-boundary drift: did any proposal blur local/dry-run work with external activation?

## Public export rules

When publishing governance derived from private projects:

1. Replace machine-specific paths with `<project-root>` or `<obsidian-project-namespace>`.
2. Replace account names, aliases, organizations, target names, and dataset names with placeholders.
3. Remove raw logs, credentials, tokens, generated artifacts, and private evidence.
4. Preserve the process pattern, not the private project facts.
5. Run a safety scan before commit and before push.
