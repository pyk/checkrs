"""Implementation of the ``lints`` command."""

from __future__ import annotations

import sys

from checkrs.lints import get_all_lints


def list_lints() -> None:
    """Print all registered lints with their metadata."""
    for lint in get_all_lints():
        sys.stdout.write(f"{lint.name}\n")
        sys.stdout.write(f"  {lint.description}\n")
        sys.stdout.write("\n")
