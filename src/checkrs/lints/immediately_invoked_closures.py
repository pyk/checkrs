"""Lint: immediately-invoked closures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class ImmediatelyInvokedClosures(Lint):
    """immediately-invoked closures."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "immediately_invoked_closures"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return (
            "using immediately-invoked closures like (|| { ... })(). Define a"
            "dedicated function instead"
        )

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Immediately-invoked closures like (|| { ... })() are cryptic and"
            "make the code harder to read. Instead, define a named function or a"
            "local function with the `fn` keyword."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Bad: ```rust let result = (|| { Ok(()) })(); ```"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\nlet result = (|| {\n    Ok(())\n})();\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "define a named function instead of immediately-invoked closures"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {"pattern": "(|| { $$$STATEMENTS })()"},
                    {"pattern": "(|| $EXPR)()"},
                    {"pattern": "(move || { $$$STATEMENTS })()"},
                    {"pattern": "(move || $EXPR)()"},
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
