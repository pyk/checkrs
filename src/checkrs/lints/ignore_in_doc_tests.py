"""Lint: ignore attributes in doc tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class IgnoreInDocTests(Lint):
    """ignore attributes in doc tests."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "ignore_in_doc_tests"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "ignore attributes in doc tests"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "The `ignore` attribute completely skips doc test validation, which"
            "can hide compilation errors and typos. Use `no_run` to ensure the"
            "code compiles without executing it."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Replace: ```rust /// ```ignore /// let x = 1; /// ``` ```"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n/// ```ignore\n/// let x = 1;\n/// ```\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "use no_run instead of ignore in doc tests"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"kind": "line_comment", "regex": "```ignore"},
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
