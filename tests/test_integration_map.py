from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts import integration_map, mpmg


class IntegrationMapTests(unittest.TestCase):
    def test_detects_existing_tools_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("# Claude instructions\n", encoding="utf-8")
            (root / ".sopify").mkdir()
            (root / "openspec").mkdir()
            (root / "memory-bank").mkdir()
            (root / "memory-bank" / "projectbrief.md").write_text("# Brief\n", encoding="utf-8")
            (root / "memory-bank" / "activeContext.md").write_text("# Active\n", encoding="utf-8")

            before = {
                path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in root.rglob("*")
                if path.is_file()
            }

            report = integration_map.inspect(root)
            names = {item["name"] for item in report["detected_surfaces"]}
            after = {
                path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in root.rglob("*")
                if path.is_file()
            }

            self.assertTrue(report["read_only"])
            self.assertEqual(before, after)
            self.assertIn("AGENTS.md", names)
            self.assertIn("CLAUDE.md", names)
            self.assertIn(".sopify", names)
            self.assertIn("openspec", names)
            self.assertIn("Cline-style memory bank", names)
            self.assertTrue(
                all(item["status"] == "observed" and item["evidence"] for item in report["detected_surfaces"])
            )
            self.assertFalse((root / ".mpmg").exists())

    def test_json_output_has_stable_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(integration_map.main([tmp, "--format", "json"]), 0)
            report = json.loads(output.getvalue())
            self.assertEqual(report["schema_version"], "mpmg.integration-map.v1")
            self.assertEqual(
                report["scan_scope"],
                {"target_only": True, "follow_external_links": False},
            )
            self.assertIn("current_observed_state", report["overlay_contract"])
            self.assertIn("intended_behavior", report["overlay_contract"])
            self.assertTrue(any("does not prove" in item for item in report["limitations"]))

    def test_optional_write_creates_only_authority_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(integration_map.main([tmp, "--write"]), 0)
            authority_map = root / ".mpmg" / "authority-map.md"
            self.assertTrue(authority_map.is_file())
            self.assertEqual(
                [path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()],
                [".mpmg/authority-map.md"],
            )
            saved = authority_map.read_text(encoding="utf-8")
            self.assertIn("Thin overlay contract", saved)
            self.assertIn("proposed-not-authoritative", saved)
            self.assertNotIn(str(root), saved)

    def test_unified_cli_exposes_read_only_integration_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(mpmg.main(["integration-map", tmp, "--format", "markdown"]), 0)
            self.assertIn("AI Context Integration Map", output.getvalue())
            self.assertFalse((Path(tmp) / ".mpmg").exists())

    def test_default_json_write_uses_json_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(
                    integration_map.main([tmp, "--format", "json", "--write"]),
                    0,
                )
            path = Path(tmp) / ".mpmg" / "authority-map.json"
            self.assertTrue(path.is_file())
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["root"], ".")
            detected = integration_map.inspect(Path(tmp))["detected_surfaces"]
            self.assertTrue(any(item["kind"] == "mpmg-overlay" for item in detected))

    def test_write_cannot_escape_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp).parent / "outside-authority-map.md"
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    integration_map.main([tmp, "--write", str(outside)])
            self.assertFalse(outside.exists())

    def test_write_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "map.md"
            destination.write_text("keep me\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    integration_map.main([tmp, "--write", "map.md"])
            self.assertEqual(destination.read_text(encoding="utf-8"), "keep me\n")

    def test_unicode_target_is_supported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "專案 with space"
            root.mkdir()
            (root / "AGENTS.md").write_text("# Instructions\n", encoding="utf-8")

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(integration_map.main([str(root), "--format", "json"]), 0)
            report = json.loads(output.getvalue())
            self.assertEqual(report["detected_surfaces"][0]["name"], "AGENTS.md")

    def test_external_directory_symlink_is_not_followed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(tmp)
            outside = Path(outside_tmp)
            (outside / "AGENTS.md").write_text("# External\n", encoding="utf-8")
            link = root / "external-link"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")

            report = integration_map.inspect(root)
            self.assertEqual(report["detected_surfaces"], [])


if __name__ == "__main__":
    unittest.main()
