# Quickstart

This path is for someone who wants to try the kit in five minutes.

## 1. See the pain first

```bash
python scripts/mpmg.py doctor examples/agent-chaos-before-after/before || true
python scripts/mpmg.py doctor examples/agent-chaos-before-after/after
python scripts/mpmg.py validate-artifacts examples/agent-chaos-before-after/after
```

The first command intentionally fails. It shows the kind of project-context drift this kit is meant to catch.

## 2. Validate this repo

```bash
python scripts/mpmg.py doctor .
```

## 3. Generate a governed demo project

```bash
python scripts/mpmg.py init   --target /tmp/mpmg-demo   --project-name DemoProject   --notes-namespace notes/Projects/DemoProject   --force
```

## 4. Audit it

```bash
python scripts/mpmg.py audit /tmp/mpmg-demo --format markdown
```

## 5. Generate a worker task

```bash
python scripts/mpmg.py worker-task   --target /tmp/mpmg-demo   --name review-routing   --task "Review memory routing and propose the next safe cleanup"   --scope handoff/   --read notes/Projects/DemoProject/00_Index.md   --validation "python scripts/validate_governance.py ."
```

## 6. Plan handoff cleanup

```bash
python scripts/mpmg.py plan-handoff-cleanup /tmp/mpmg-demo --format markdown
```

The output is a plan, not an automatic move. It is intentionally safe by default.
