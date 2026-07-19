from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import integration_map, mpmg


class IntegrationMapTests(unittest.TestCase):
    def test_detects_existing_tools_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("# Agent instructions\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("# Claude instructions\n", encoding="utf-8")
            (root / ".hermes.md").write_text("# Hermes context\n", encoding="utf-8")
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
            self.assertIn(".hermes.md", names)
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

    def test_hermes_context_counts_as_shared_repository_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".hermes.md").write_text("# Project context\n", encoding="utf-8")
            report = integration_map.inspect(root)
            self.assertIn(".hermes.md", {item["name"] for item in report["detected_surfaces"]})
            self.assertNotIn(
                "No shared repository instruction file was detected; decide whether one is needed.",
                report["questions_to_resolve"],
            )

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
            self.assertIn("Artifact written: `.mpmg/authority-map.md`", saved)
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
            root = Path(tmp)
            outside = root.parent / f"{root.name}-outside-authority-map.md"
            for write_value in (str(outside), f"../{outside.name}"):
                with self.subTest(write_value=write_value):
                    with contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit):
                            integration_map.main([tmp, "--write", write_value])
            self.assertFalse(outside.exists())

    def test_write_rejects_external_mpmg_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(tmp)
            outside = Path(outside_tmp)
            try:
                (root / ".mpmg").symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    integration_map.main([tmp, "--write"])
            self.assertFalse((outside / "authority-map.md").exists())

    def test_write_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / ".mpmg" / "map.md"
            destination.parent.mkdir()
            destination.write_text("keep me\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    integration_map.main([tmp, "--write", ".mpmg/map.md"])
            self.assertEqual(destination.read_text(encoding="utf-8"), "keep me\n")

    def test_force_cannot_overwrite_context_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            context_file = Path(tmp) / "AGENTS.md"
            context_file.write_text("# Keep this\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    integration_map.main([tmp, "--write", "AGENTS.md", "--force"])
            self.assertEqual(context_file.read_text(encoding="utf-8"), "# Keep this\n")

    def test_force_requires_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    integration_map.main([tmp, "--force"])

    def test_markdown_escapes_repository_controlled_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = integration_map.inspect(Path(tmp))
            report["detected_surfaces"] = [
                {
                    "name": "repo-instructions",
                    "kind": "repo-instructions",
                    "paths": ["bad|`<x>/AGENTS.md"],
                    "evidence": ["bad|`<x>/AGENTS.md"],
                    "status": "observed",
                    "basis": "repository_path_signature",
                    "guidance": "untrusted | guidance <here>",
                }
            ]
            rendered = integration_map.render_markdown(report)
            self.assertIn("bad\\|&#96;&lt;x&gt;/AGENTS.md", rendered)
            self.assertIn("untrusted \\| guidance &lt;here&gt;", rendered)

    def test_scan_errors_are_reported_without_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()

            def failing_walk(path, *, onerror, followlinks):
                self.assertFalse(followlinks)
                onerror(PermissionError(13, "Access denied", str(root / "blocked")))
                return []

            with mock.patch("scripts.integration_map.os.walk", side_effect=failing_walk):
                report = integration_map.inspect(root)
            self.assertEqual(report["scan_warnings"], ["Could not scan `blocked`: Access denied."])

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
