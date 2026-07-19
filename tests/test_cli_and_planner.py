from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import init_governance, mpmg, plan_handoff_cleanup


class CliAndPlannerTests(unittest.TestCase):
    def test_unified_cli_init_validate_doctor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(mpmg.main(["init", "--target", str(root), "--project-name", "Demo", "--notes-namespace", "notes/Projects/Demo"]), 0)
            self.assertEqual(mpmg.main(["validate", str(root)]), 0)
            self.assertEqual(mpmg.main(["doctor", str(root), "--format", "json"]), 0)

    def test_handoff_cleanup_plan_classifies_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_governance.main(["--target", str(root), "--project-name", "Demo", "--notes-namespace", "notes/Projects/Demo"])
            review = root / "handoff" / "old_review.md"
            review.write_text("# Review\n", encoding="utf-8")
            report = plan_handoff_cleanup.plan(root)
            categories = {item["path"]: item["category"] for item in report["entries"]}
            self.assertEqual(categories["handoff/old_review.md"], "reviews")


if __name__ == "__main__":
    unittest.main()
