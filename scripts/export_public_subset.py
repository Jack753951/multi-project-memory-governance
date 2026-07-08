#!/usr/bin/env python
"""Create a public governance export subset and run the safety scan."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import check_public_safety

INCLUDE = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "pyproject.toml",
    "docs",
    "templates",
    "examples",
    "skills",
    "scripts",
    "tests",
    ".github",
]


def copy_item(src: Path, dst: Path) -> None:
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    elif src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Export directory")
    parser.add_argument("--force", action="store_true", help="Delete output first if it exists")
    args = parser.parse_args(argv)
    output = Path(args.output).resolve()
    if output.exists() and args.force:
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    for rel in INCLUDE:
        copy_item(ROOT / rel, output / rel)
    code = check_public_safety.main_for_path(output) if hasattr(check_public_safety, "main_for_path") else None
    if code is None:
        import sys
        old = sys.argv[:]
        sys.argv = ["check_public_safety.py", str(output)]
        try:
            code = check_public_safety.main()
        finally:
            sys.argv = old
    if code == 0:
        print(f"Export ready: {output}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
