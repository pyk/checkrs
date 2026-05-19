"""Lint: self:: imports."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class SelfImports(Lint):
    """self:: imports."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "self_imports"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "self:: imports"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using self:: in use statements is redundant. Items in the current"
            "module can be used directly. Consider removing self:: to improve"
            "code clarity."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Using self:: in use statements is redundant. Items in the current"
            "module can be used directly. Consider removing self:: to improve"
            "code clarity."
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
        return "import items directly instead of using self::"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"all": [{"kind": "use_declaration"}, {"regex": "\\buse\\s+self::"}]},
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
