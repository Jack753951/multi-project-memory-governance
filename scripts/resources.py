"""Locate repository resources in a source checkout or an installed wheel."""
from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
SOURCE_ROOT = PACKAGE_DIR.parent
INSTALLED_KIT_ROOT = PACKAGE_DIR / "_kit"


def resource_path(relative: str) -> Path:
    """Return a kit path from a checkout first, then from bundled wheel data."""
    in_source_checkout = (SOURCE_ROOT / "pyproject.toml").is_file() and (SOURCE_ROOT / "scripts").resolve() == PACKAGE_DIR
    if in_source_checkout:
        source = SOURCE_ROOT / relative
        if source.exists():
            return source
    if relative == "scripts":
        return PACKAGE_DIR
    bundled = INSTALLED_KIT_ROOT / relative
    if bundled.exists():
        return bundled
    raise FileNotFoundError(f"packaged resource is unavailable: {relative}")
