"""Lint: extra space after period in comments."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class ExtraSpaceAfterPeriod(Lint):
    """extra space after period in comments."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "extra_space_after_period"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "comments with extra space after period"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Flags line comments that contain a period followed by two or"
            " more spaces."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Extra spaces after periods are unnecessary and inconsistent"
            " with modern typographic style. Use a single space."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "    /// A single transaction can interleave multiple"
            " `vm.coinbase` calls and\n"
            "    /// end on the expected address without corrupting state."
            "  This proves the\n"
            "    /// cheatcode is deterministic and safe to call"
            " repeatedly inside one tx.\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use a single space after a period"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "line_comment"},
                    {"regex": r"\.[ \t]{2,}"},
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
