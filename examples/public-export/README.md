# Public Export Example

This synthetic example shows the intended public-export flow.

## Flow

1. Extract process patterns, not private project state.
2. Replace local paths, accounts, targets, artifacts, and run IDs with placeholders.
3. Run public safety scan.
4. Publish only docs/templates/examples/tools that are meant to be reusable.

## Command

```bash
python scripts/mpmg.py export-public --output /tmp/mpmg-export --force
python scripts/mpmg.py safety-scan /tmp/mpmg-export
```

The export helper is intentionally conservative and should be paired with human review before publishing.
