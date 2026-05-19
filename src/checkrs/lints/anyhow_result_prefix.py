"""Lint: import anyhow::Result instead of using the fully qualified path."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AnyhowResultPrefix(Lint):
    """anyhow::Result fully-qualified paths."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_result_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "anyhow::Result used with fully qualified path"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for `anyhow::Result` written as a fully qualified path"
            "instead of being imported and used as `Result`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Importing `anyhow::Result` keeps return types concise and"
            "consistent with project conventions."
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
            "pub fn create_database(&self) -> anyhow::Result<Database> {\n"
            "    // ...\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "import anyhow::Result and use it without the anyhow:: prefix"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "scoped_type_identifier"},
                    {"regex": "anyhow::Result"},
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
