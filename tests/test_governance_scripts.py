from __future__ import annotations

import contextlib
import io
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

    def test_init_preserves_selected_existing_context_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agents = root / "AGENTS.md"
            agents.write_text("# Existing instructions\n", encoding="utf-8")
            self.assertEqual(
                init_governance.main(
                    [
                        "--target",
                        str(root),
                        "--project-name",
                        "Demo",
                        "--notes-namespace",
                        "notes/Projects/Demo",
                        "--context-file",
                        "AGENTS.md",
                    ]
                ),
                0,
            )
            self.assertEqual(agents.read_text(encoding="utf-8"), "# Existing instructions\n")
            self.assertFalse((root / ".hermes.md").exists())

    def test_init_rejects_paths_outside_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "outside-notes"
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    init_governance.main(
                        [
                            "--target",
                            str(root),
                            "--project-name",
                            "Demo",
                            "--notes-namespace",
                            str(outside),
                        ]
                    )
            self.assertFalse(outside.exists())


if __name__ == "__main__":
    unittest.main()
