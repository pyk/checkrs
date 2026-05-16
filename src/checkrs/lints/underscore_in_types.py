"""Lint: underscores in type annotations."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class UnderscoreInTypes(Lint):
    """underscores in type annotations."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "underscore_in_types"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "underscores in type annotations"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "When you annotate a type explicitly, use the actual type instead of"
            "_. If you want type inference, omit the type annotation entirely."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Instead of: ```rust let items: Vec<_> = values.collect(); ```"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\nlet items: Vec<_> = values.collect();\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "specify the actual type instead of underscore"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {"kind": "type_identifier", "regex": "^_$"},
                    {"regex": "^_$", "follows": {"regex": "^<$"}},
                ],
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
