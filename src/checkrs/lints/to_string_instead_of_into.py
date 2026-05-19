"""Lint: to_string() where into() suffices."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class ToStringInsteadOfInto(Lint):
    """to_string() where into() suffices."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "to_string_instead_of_into"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "to_string() where into() suffices"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "The `.into()` method is more idiomatic Rust when converting to"
            "String. It works for types like `&str`, `String`, `&String`,"
            "`PathBuf`, `Path`, etc."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Note: `.to_string()` works on any type implementing `Display`, while"
            "`.into()` requires an explicit `Into<String>` implementation. This"
            "rule may produce false positives for types that don't implement"
            "`Into<String>`."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "Note: `.to_string()` works on any type implementing `Display`, while"
            "`.into()` requires an explicit `Into<String>` implementation. This"
            "rule may produce false positives for types that don't implement"
            "`Into<String>`."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n// No example provided\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "use into() instead of to_string() when possible"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"pattern": "$EXPR.to_string()"},
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
