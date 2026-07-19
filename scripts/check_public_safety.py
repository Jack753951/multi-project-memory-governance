#!/usr/bin/env python
"""Simple public-export safety scan.

This is not a secret detector replacement. It catches obvious private paths,
common token labels, and placeholder mistakes before publishing.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

PATTERNS = [
    ("windows_user_path", re.compile(r"[A-Za-z]:(?:\\+|/)Users(?:\\+|/)[^\\/\s\"]+", re.I)),
    ("unix_home_path", re.compile(r'/home/[^\s`\'\"]+', re.I)),
    ("private_env_assignment", re.compile(r'\b(?:API_KEY|TOKEN|SECRET|PASSWORD|COOKIE)\s*=\s*[^\s]+', re.I)),
    ("github_token", re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}')),
    ("openai_key", re.compile(r'sk-[A-Za-z0-9_-]{20,}')),
    ("aws_access_key", re.compile(r'AKIA[0-9A-Z]{16}')),
]

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "build", "dist"}
TEXT_EXTS = {".md", ".txt", ".py", ".yaml", ".yml", ".json", ".toml", ".gitignore"}


def is_text_candidate(path: Path) -> bool:
    return path.name in {"LICENSE", "README"} or path.suffix.lower() in TEXT_EXTS


def scan(root: Path):
    findings = []

    def skip_directory(name: str) -> bool:
        return (
            name in SKIP_DIRS
            or name.startswith(".build-test")
            or name.endswith(".egg-info")
        )

    def onerror(exc: OSError) -> None:
        path = Path(exc.filename) if exc.filename else root
        findings.append((path, 0, "scan_error", exc.strerror or type(exc).__name__))

    for current, dirs, files in os.walk(root, onerror=onerror, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(
            name
            for name in dirs
            if not skip_directory(name) and not (current_path / name).is_symlink()
        )
        for filename in sorted(files):
            path = current_path / filename
            if path.is_symlink() or not is_text_candidate(path):
                continue
            if path.name == "check_public_safety.py":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            except OSError as exc:
                findings.append((path, 0, "scan_error", exc.strerror or type(exc).__name__))
                continue
            for line_no, line in enumerate(text.splitlines(), 1):
                for name, pattern in PATTERNS:
                    if pattern.search(line):
                        findings.append((path, line_no, name, line.strip()[:160]))

    return findings


def main_for_path(root: Path) -> int:
    findings = scan(root)
    if findings:
        print("Potential public-safety findings:")
        for path, line_no, name, snippet in findings:
            print(f"{path}:{line_no}: {name}: {snippet}")
        return 1
    print("No obvious private path/token patterns found.")
    return 0


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    return main_for_path(root)


if __name__ == "__main__":
    raise SystemExit(main())
