"""Lint: import InMemoryDB instead of using the fully qualified path."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class RevmDatabaseInmemorydbPrefix(Lint):
    """revm::database::InMemoryDB fully-qualified paths."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "revm_database_inmemorydb_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "revm::database::InMemoryDB used with fully qualified path"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for `revm::database::InMemoryDB` written as a fully qualified"
            "path instead of being imported and used as `InMemoryDB`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Importing `revm::database::InMemoryDB` keeps type signatures concise"
            "and consistent with project conventions."
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
            "pub fn create_db() -> revm::database::InMemoryDB {\n"
            "    // ...\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "import InMemoryDB and use it without the revm::database:: prefix"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {
                        "all": [
                            {"kind": "scoped_type_identifier"},
                            {"regex": "revm::database::InMemoryDB"},
                        ]
                    },
                    {
                        "all": [
                            {"kind": "call_expression"},
                            {"regex": "revm::database::InMemoryDB::"},
                        ]
                    },
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
