from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts import check_public_safety


class PublicSafetyTests(unittest.TestCase):
    def test_wheel_prefixed_file_is_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_path = "C:" + "\\Users\\ExampleUser\\private-project"
            (root / ".wheel-map.json").write_text(
                json.dumps({"root": private_path}) + "\n",
                encoding="utf-8",
            )
            findings = check_public_safety.scan(root)
            self.assertTrue(any(item[2] == "windows_user_path" for item in findings))

    def test_wheel_prefixed_directory_is_not_a_scan_bypass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            generated = root / ".wheel-smoke"
            generated.mkdir()
            private_path = "C:" + "\\Users\\ExampleUser\\private-project"
            (generated / "report.json").write_text(
                json.dumps({"root": private_path}) + "\n",
                encoding="utf-8",
            )
            findings = check_public_safety.scan(root)
            self.assertTrue(any(item[2] == "windows_user_path" for item in findings))


if __name__ == "__main__":
    unittest.main()
