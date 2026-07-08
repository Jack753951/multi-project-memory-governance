from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import validate_artifacts


class ArtifactValidatorTests(unittest.TestCase):
    def test_multi_agent_example_artifacts_pass(self) -> None:
        root = Path("examples/multi-agent-review")
        report = validate_artifacts.validate(root)
        self.assertTrue(report["passed"])
        self.assertGreaterEqual(report["artifacts_checked"], 2)

    def test_missing_review_identity_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            review_dir = root / "handoff" / "reviews"
            review_dir.mkdir(parents=True)
            (review_dir / "bad.md").write_text("# Review\n\nNo identity.\n", encoding="utf-8")
            report = validate_artifacts.validate(root)
            self.assertFalse(report["passed"])
            self.assertIn("## Reviewer identity", report["results"][0]["missing"])


if __name__ == "__main__":
    unittest.main()
