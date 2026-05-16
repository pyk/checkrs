"""Registered checkrs lints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.mod_rs_missing_docs import ModRsMissingDocs

if TYPE_CHECKING:
    from checkrs.lints.lint import Lint


def get_all_lints() -> list[Lint]:
    """Return all registered lints."""
    return [
        ModRsMissingDocs(),
    ]
