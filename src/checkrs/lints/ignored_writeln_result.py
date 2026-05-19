"""Lint: ignored writeln! results."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class IgnoredWritelnResult(Lint):
    """ignored writeln! results."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "ignored_writeln_result"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "ignored writeln! results"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Discarding the `Result` returned by `writeln!` hides write errors."
            "Use the `?` operator to propagate the error to the caller:"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Incorrect:** ```/dev/null/incorrect.rs#L1-3 let _ ="
            'writeln!(output, "### {}", action.name); let _ = writeln!(output);'
            "```"
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n\n**Correct:**\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "propagate writeln! errors with `?`"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"pattern": "let _ = writeln!($$$ARGS)"},
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
