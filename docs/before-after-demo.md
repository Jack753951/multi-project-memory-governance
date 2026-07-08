# Before/After Demo: Stop AI Agents from Mixing Up Projects

This demo is the fastest way to understand the project.

The problem is not "memory" in the abstract. The problem is that long-running AI coding agents start trusting the wrong layer of context:

- chat history instead of repo files;
- global memory instead of project handoff;
- stale notes instead of current strategy;
- worker outputs with no required-read list;
- reviews with no model/tool/limitation metadata.

## Run the unhealthy project

```bash
python scripts/mpmg.py doctor examples/agent-chaos-before-after/before
python scripts/mpmg.py plan-handoff-cleanup examples/agent-chaos-before-after/before --format markdown
```

You should see governance failures such as missing required handoff files, missing `Required reads`, and missing worker/review structure.

## Run the governed project

```bash
python scripts/mpmg.py doctor examples/agent-chaos-before-after/after
python scripts/mpmg.py validate-artifacts examples/agent-chaos-before-after/after
```

You should see a passing doctor report and passing worker/review artifact metadata.

## What changed

| Before | After |
|---|---|
| Agent told to use old notes and chat history | Agent gets explicit required reads |
| Handoff folder is a dumping ground | Handoff index points to current truth |
| Review has no identity metadata | Review records route/tool/model visibility/focus/limitations |
| Worker scope is implicit | Worker task lists allowed scope and disallowed actions |
| Public export is a vague reminder | Safety scan is a repeatable command |

This kit is not a memory database. It is an authority-boundary and hygiene kit for AI-assisted projects.
