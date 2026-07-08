# Contributing

Thanks for improving this governance kit.

## Principles

- Preserve process patterns, not private project state.
- Do not add real credentials, accounts, targets, paths, raw logs, client data, or run-specific evidence.
- Prefer small, composable templates and scripts over large one-off policy documents.
- If a rule is reusable, put it in docs/templates/skills. If it is project-specific, it belongs in an example or downstream project.

## Development

Run the local checks before opening a PR:

```bash
python -m unittest discover -s tests
python scripts/validate_governance.py examples/minimal-project
python scripts/check_public_safety.py .
```

## Pull request checklist

- [ ] New docs explain when to use them and when not to use them.
- [ ] New templates avoid private paths and project-specific assumptions.
- [ ] Scripts have tests or a clear manual validation path.
- [ ] Public safety scan passes.
