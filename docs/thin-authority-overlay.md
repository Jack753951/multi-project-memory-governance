# Thin Authority Overlay

MPMG works best as a small compatibility layer between context systems that already exist in a project. It should not replace `AGENTS.md`, `CLAUDE.md`, Cline Memory Bank, Sopify, Spec Kit, OpenSpec, Ruler, a memory backend, or a runtime policy engine.

Its job is narrower:

1. inventory the context surfaces already present;
2. name the role and scope of each surface;
3. expose authority seams that a project owner must resolve;
4. keep memory and handoff material from silently overriding fresher evidence;
5. make external-worker inputs explicit.

## Start read-only

From the MPMG repository, inspect an existing project without changing it:

```bash
python scripts/mpmg.py integration-map /path/to/project
```

Use JSON when another tool will consume the result:

```bash
python scripts/mpmg.py integration-map /path/to/project --format json
```

The command recognizes common repository-local surfaces, including:

- `AGENTS.md`, `CLAUDE.md`, Claude/Cursor scoped rules, and Copilot instructions;
- Ruler instruction sources;
- Sopify, Spec Kit, OpenSpec, and BMAD artifact directories;
- repo-local handoff directories;
- Cline-style Memory Bank files;
- Obsidian vault markers;
- an existing MPMG authority declaration.

Detection is based on paths and filenames. It does **not** prove that a file is current, correct, authoritative, or actually read by an agent.

## Optional one-file overlay

If the report is useful, save it as one reviewable file:

```bash
python scripts/mpmg.py integration-map /path/to/project --write
```

This writes only:

```text
.mpmg/authority-map.md
```

It does not modify existing instructions, specifications, memory files, handoffs, or tool configuration. Existing files are not overwritten unless `--force` is explicitly provided.

Treat the generated map as a discussion and review artifact. A project owner must still answer its unresolved questions.

## Give each tool a narrow role

| Existing system | Suggested role | What MPMG adds between systems |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md`, scoped rules | Normative agent instructions | Scope boundaries and conflict questions |
| Ruler | Distribute shared instructions | A reminder that synchronization does not make every rule global |
| Cline Memory Bank or project memory | Durable project context | Freshness and re-verification boundary |
| Sopify or repo handoff | Current work state, decisions, evidence | One named owner for active state and explicit worker reads |
| Spec Kit or OpenSpec | Intended behavior and accepted requirements | A way to identify implementation/spec drift without silently choosing one |
| Obsidian or project notes | Long-term rationale and research | Links to current repo truth instead of duplicated status |
| Mem0, Letta, Graphiti, or agent auto-memory | Recall, personalization, discovery | Scope and authority limits; changing facts require verification |
| Tandem, hooks, approvals, or policy runtime | Enforced permissions and gates | Documentation of why a boundary exists; MPMG does not replace enforcement |

## Two kinds of truth

A single linear precedence list is not sufficient for every disagreement.

### Current observed state

For questions such as "what code is deployed?" or "which tests pass now?", prefer:

1. live files, configuration, and fresh validation evidence;
2. verified current handoff;
3. project notes and memory as leads that require verification.

Current explicit operator instruction controls the task and scope, but cannot make an unverified statement about the system's present state become true.

### Intended behavior

For questions such as "what should this feature do?", an accepted specification or policy may be authoritative even when the implementation differs.

That disagreement is **drift to resolve**. Do not silently declare either the stale implementation or the stale specification correct. Record the conflict, identify the owner, and verify which artifact must change.

## Adoption levels

### Level 0: inspect only

Run `integration-map` and keep no generated file. Use this when evaluating a project or diagnosing context confusion.

### Level 1: one-file overlay

Commit `.mpmg/authority-map.md` after a human reviews and edits it. Keep all existing tools in place.

### Level 2: selective contracts

Add only the missing boundary, such as explicit worker required reads, handoff freshness metadata, or a project-notes pointer.

### Level 3: full governance kit

Use `mpmg init` only when a long-running or multi-agent project genuinely needs the complete handoff, review, notes, and validation layout.

## Non-goals

The overlay does not:

- merge or rewrite third-party configuration;
- infer semantic truth from filenames;
- guarantee that an agent obeyed an instruction;
- replace hooks, permissions, approval gates, or secret scanners;
- require every project to adopt the full MPMG file structure;
- become another store for duplicated project state.
