# Related Work and Integration Boundaries

MPMG is not a replacement for mature instruction, memory, specification, handoff, or runtime-governance systems. It is a thin authority overlay between them.

## Existing systems already solve important layers

| Layer | Mature examples | What they own | Boundary MPMG can clarify |
|---|---|---|---|
| Repository instructions | [AGENTS.md](https://agents.md/), [Claude Code memory and CLAUDE.md](https://code.claude.com/docs/en/memory) | Agent instructions, nested/path scope, user or project rules | Which rules are shared, local, generated, or directory-scoped; instructions are context unless separately enforced |
| Cross-agent instruction distribution | [Ruler](https://github.com/intellectronica/ruler) | Author one rule set and distribute it to several coding assistants | Synchronization does not make every rule authoritative at every scope |
| Project memory | [Cline Memory Bank](https://docs.cline.bot/best-practices/memory-bank), [Project Butler](https://github.com/JamesShi96/project-butler) | Durable project context and cross-session continuity | Changing facts require freshness checks; memory is not automatically current state |
| Handoff, plans, and evidence | [Sopify](https://github.com/evidentloop/sopify) | Cross-agent work continuity, decisions, and verification evidence | Name one owner for current work state and declare required reads for workers |
| Specifications and change artifacts | [Spec Kit](https://github.com/github/spec-kit), [OpenSpec](https://github.com/Fission-AI/OpenSpec), [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | Intended behavior, plans, tasks, and reviewable change intent | Separate normative truth from observed implementation; expose drift instead of silently choosing one |
| Memory backends | [Mem0](https://github.com/mem0ai/mem0), [Letta](https://github.com/letta-ai/letta), [Graphiti](https://github.com/getzep/graphiti) | Memory storage, retrieval, temporal knowledge, and personalization | Retrieved memory still needs project scope, freshness, and authority limits |
| Runtime governance | [Tandem](https://github.com/frumu-ai/tandem), tool hooks, permission and approval systems | Enforced actions, approvals, tenant boundaries, and audit trails | Document why a boundary exists; MPMG does not turn prompt text into enforcement |

These projects have stronger adoption, product maturity, or depth in their own categories. MPMG should compose with them rather than reproduce their features.

## The remaining seam

When several layers are present at once, a project still needs to answer:

- Which source owns current observed state?
- Which source owns intended behavior?
- Which handoff or workflow artifact owns active work state?
- Which instructions are global, repository-scoped, path-scoped, or local?
- Which memory sources are recall aids only?
- What must an external worker read explicitly?
- Who resolves a conflict, and what evidence is required?

MPMG's narrow role is to make those questions visible and keep the answers reviewable.

## Design consequences

1. **Inspect before generating.** `mpmg integration-map` is read-only by default.
2. **Add one small overlay before a full layout.** `--write` creates only `.mpmg/authority-map.md`.
3. **Do not rewrite third-party files.** Existing tools keep ownership of their formats and behavior.
4. **Do not claim semantic inference.** Filename detection cannot prove freshness, correctness, or actual agent compliance.
5. **Separate observed and intended truth.** Live validation answers what is happening; accepted specifications and policies answer what should happen. Their mismatch is drift to resolve.
6. **Leave enforcement to enforcement systems.** Hooks, permissions, approvals, and runtime policy remain outside MPMG.

## Honest scope

MPMG combines practices that already exist separately; it does not claim to have invented project-local instructions, persistent project memory, handoff artifacts, specification-driven development, or runtime governance.

Its contribution is the compatibility contract between those practices:

> When more context systems are connected to an agent, specify what each one may be trusted for and how conflicts become visible.

There is not yet evidence that MPMG is a broadly adopted standard. Treat it as an early, inspectable method and tool, validate it in real projects, and keep only the parts that reduce confusion.
