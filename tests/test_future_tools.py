from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import governance_audit, init_governance, new_worker_task


class FutureToolTests(unittest.TestCase):
    def test_audit_passes_initialized_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_governance.main([
                "--target", str(root),
                "--project-name", "Demo",
                "--notes-namespace", "notes/Projects/Demo",
            ])
            report = governance_audit.audit(root)
            self.assertTrue(report["validation_passed"])
            self.assertTrue(report["public_safety_passed"])

    def test_new_worker_task_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            code = new_worker_task.main([
                "--target", str(root),
                "--name", "Review Routing",
                "--task", "Review memory routing boundaries.",
                "--scope", "handoff/",
                "--read", "docs/architecture.md",
                "--validation", "python scripts/validate_governance.py .",
                "--worker-tool", "test-worker",
            ])
            self.assertEqual(code, 0)
            files = list((root / "handoff" / "worker_tasks").glob("*_review-routing.md"))
            self.assertEqual(len(files), 1)
            text = files[0].read_text(encoding="utf-8")
            self.assertIn("Review memory routing boundaries.", text)
            self.assertIn("docs/architecture.md", text)
            self.assertIn("test-worker", text)


if __name__ == "__main__":
    unittest.main()
