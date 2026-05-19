"""Lint: context(format!()) instead of with_context."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AnyhowContextFormat(Lint):
    """context(format!()) instead of with_context."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_context_format"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "context(format!()) instead of with_context"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using `with_context` with a closure is more efficient because the"
            "format string is only evaluated when an error occurs. With"
            "`context`, the format string is evaluated eagerly, even when the"
            "operation succeeds."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            'Instead of: ```rust result.context(format!("Failed to process:'
            '{:?}", input))?; ```'
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            '```rust\nresult.context(format!("Failed to process: {:?}", input))?;\n```'
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use with_context(|| format!()) instead of context(format!())"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"pattern": "$EXPR.context(format!($$$ARGS))"},
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
