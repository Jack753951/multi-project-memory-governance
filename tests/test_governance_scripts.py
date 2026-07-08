from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import init_governance, validate_governance


class GovernanceScriptTests(unittest.TestCase):
    def test_init_then_validate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".hermes.md").write_text(
                "# Context\n\n## Required reads every session\n\n"
                "External workers must not assume access to global durable memory.\n",
                encoding="utf-8",
            )
            code = init_governance.main([
                "--target", str(root),
                "--project-name", "Demo",
                "--notes-namespace", "notes/Projects/Demo",
            ])
            self.assertEqual(code, 0)
            self.assertFalse(validate_governance.validate(root))

    def test_validator_catches_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate_governance.validate(Path(tmp))
            self.assertTrue(any("missing required file" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
