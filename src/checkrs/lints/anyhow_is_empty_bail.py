"""Lint: is_empty() followed by bail! in if blocks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class AnyhowIsEmptyBail(Lint):
    """is_empty() followed by bail! in if blocks."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_is_empty_bail"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "is_empty() followed by bail! in if blocks"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using `ensure!` with `!is_empty()` is more concise and readable than"
            "checking `is_empty()` with a `bail!` in an if statement."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Incorrect:** ```rust if name.trim().is_empty() {"
            'anyhow::bail!("Contract identifier name cannot be empty"); } ```'
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
            "if name.trim().is_empty() {\n"
            '    anyhow::bail!("Contract identifier name cannot be empty");\n'
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use ensure! with is_empty() instead of if/bail!"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {"pattern": "if $EXPR.is_empty() { bail!($$$ARGS); }"},
                    {"pattern": "if $EXPR.is_empty() { anyhow::bail!($$$ARGS); }"},
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
