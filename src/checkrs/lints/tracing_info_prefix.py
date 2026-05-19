"""Lint: tracing::info! with prefix."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class TracingInfoPrefix(Lint):
    """tracing::info! with prefix."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "tracing_info_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "tracing::info! with prefix"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Prefer importing `tracing::info` at the top of the file and using"
            "`info!` directly."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return 'Bad: tracing::info!("message");'

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
        return "import info! and use it without the tracing:: prefix"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"pattern": "tracing::info!($$$ARGS)"},
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
