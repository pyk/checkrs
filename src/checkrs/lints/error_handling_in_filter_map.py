"""Lint: error handling in filter_map closures."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class ErrorHandlingInFilterMap(Lint):
    """error handling in filter_map closures."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "error_handling_in_filter_map"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "error handling in filter_map closures"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using `filter_map` to combine filtering and error handling (e.g.,"
            "returning `Some(Err(...))`) creates confusing code that mixes two"
            "different concerns."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Problem:** The code is hard to reason about because: - `None`"
            'means "filtered out" - `Some(Ok(...))` means "valid item" -'
            '`Some(Err(...))` means "error"'
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n// No example provided\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "use a for loop instead of error handling in filter_map"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "closure_expression"},
                    {"has": {"stopBy": "end", "pattern": "Some(Err($$$))"}},
                    {"inside": {"stopBy": "end", "pattern": "$X.filter_map($$$)"}},
                ]
            },
        )
        matches = list(node.find_all(config))

        return [
            Violation(
                lint_name=self.name,
                file_path=file_path,
                line=m.range().start.line + 1,
                column=m.range().start.column + 1,
                message="found",
            )
            for m in matches
        ]
