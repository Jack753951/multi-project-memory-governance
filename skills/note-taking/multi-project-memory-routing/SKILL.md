---
name: multi-project-memory-routing
description: Use when coordinating global AI memory, repo handoff files, project notes/Obsidian, skills, and session search across multiple projects without leaking project state across boundaries.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, obsidian, handoff, multi-project, governance]
    related_skills: []
---

# Multi-Project Memory Routing

## Overview

Use this skill to decide where durable knowledge belongs when one AI-agent profile is used across multiple projects. The skill is a process and judgment framework, not a project database.

Core model:

```text
Global durable memory = compact cross-project signposts.
Repo handoff = project engineering truth.
Project notes / Obsidian = long-term strategy, rationale, decisions, experiments, review synthesis.
Skills = reusable procedures and judgment criteria.
Session search = recall leads that must be verified.
```

## When to Use

Use when:

- several repos share the same agent profile or memory backend;
- a user asks where something should be remembered;
- project context must be made visible to external workers;
- handoff files, project notes, skills, and durable memory disagree;
- preparing a public/sanitized export of a private project workflow.

Do not use this skill to store project progress, private paths, target names, credentials, raw logs, or run artifacts.

## Authority Order by Question

1. **Task and scope:** current explicit user/operator instruction.
2. **Current observed state:** live project files, config, and fresh validation evidence.
3. **Intended behavior:** current accepted requirements, specifications, and policies.
4. **Accepted work state:** verified repo handoff.
5. **Long-term rationale:** project notes / Obsidian namespace.
6. **Recall and discovery:** compact global-memory signposts, then session search; verify changing facts before acting.

Current instruction controls the task but does not rewrite observed facts. Surface specification/implementation drift instead of silently choosing a side.

## Decision Tree

1. Secret, credential, private token, cookie, client-sensitive data, or unsafe target detail?
   - Store nowhere. Record only non-sensitive handling rules if needed.
2. Reusable workflow or judgment rule applicable across projects?
   - Put it in a skill or shared governance doc.
3. Stable user preference or cross-project routing/safety rule?
   - Put a compact declarative entry in durable memory.
4. Accepted engineering state, validation output, or worker coordination for one repo?
   - Put it in repo handoff.
5. Long-term project strategy, rationale, research, decision, experiment, or review synthesis?
   - Put it in project notes / Obsidian.
6. Temporary progress or one-off output?
   - Keep it in the session or a dated handoff artifact only if needed.

## External Worker Boundary

External workers do not automatically inherit the coordinator's durable memory, current chat, or full note vault. Worker tasks should explicitly name required context reads:

```text
Before editing or reviewing, read:
- <project-context-file>
- handoff/memory_governance.md
- handoff/active_strategy_queue.md
- handoff/accepted_changes.md or named artifact for this slice
- <project-notes-index> if long-term rationale matters
```

When answering status questions, distinguish:

- guaranteed included in the worker prompt;
- available on disk if the worker reads it;
- not inherited from global memory/chat.

## Public Export Checklist

- [ ] Machine-specific paths replaced with placeholders.
- [ ] Account names, aliases, organizations, and target names removed.
- [ ] Credentials, tokens, cookies, raw logs, and private evidence removed.
- [ ] Process patterns preserved without copying private project state.
- [ ] `scripts/check_public_safety.py` or equivalent scan passed.

## Common Pitfalls

1. Turning durable memory into a project database.
   - Fix: store only compact pointers and stable preferences globally.
2. Turning a skill into a project log.
   - Fix: skills contain process and judgment criteria only.
3. Treating session search as truth.
   - Fix: verify against files or active notes.
4. Letting handoff become a dumping ground.
   - Fix: maintain a compact index, active queue, archives, and category-specific destinations.
5. Assuming workers inherit context.
   - Fix: include required reads in every bounded worker task.
