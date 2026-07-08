# Release Checklist

Use this before tagging a public release.

## Pre-release

- [ ] `CHANGELOG.md` has an entry for the version.
- [ ] `pyproject.toml` version matches the intended tag.
- [ ] README quickstart still works.
- [ ] Synthetic examples validate.
- [ ] Public export smoke test passes.
- [ ] Public safety scan passes on the repo and exported subset.
- [ ] No private project paths, accounts, targets, run IDs, credentials, or sensitive logs were added.

## Verification commands

```bash
python -m py_compile scripts/*.py
python -m unittest discover -s tests
python scripts/mpmg.py validate examples/minimal-project
python scripts/mpmg.py validate examples/multi-agent-review
python scripts/mpmg.py validate-artifacts examples/multi-agent-review
python scripts/mpmg.py doctor examples/minimal-project
python scripts/mpmg.py audit examples/minimal-project --format markdown
python scripts/mpmg.py export-public --output /tmp/mpmg-export --force
python scripts/mpmg.py safety-scan /tmp/mpmg-export
python scripts/mpmg.py safety-scan .
git diff --check
```

## Tagging

```bash
git tag -a v0.3.0 -m "v0.3.0"
git push origin v0.3.0
```

If using GitHub CLI:

```bash
gh release create v0.3.0 --title "v0.3.0" --notes-file RELEASE_NOTES.md
```
