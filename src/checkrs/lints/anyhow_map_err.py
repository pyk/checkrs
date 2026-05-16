"""Lint: map_err with anyhow macros."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class AnyhowMapErr(Lint):
    """map_err with anyhow macros."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_map_err"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "map_err with anyhow macros"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "Using `bail!` is more concise and readable than `map_err` with`anyhow`."

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Instead of: ```rust let result = expr.map_err(|e|"
            'anyhow::anyhow!("message: {}", e))?; ```'
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
            'let result = expr.map_err(|e| anyhow::anyhow!("message: {}", e))?;\n'
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "avoid map_err with anyhow macros"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {"pattern": "$TRY.map_err(|$E| anyhow::anyhow!($$$ARGS))?"},
                    {"pattern": "$TRY.map_err(|$E| anyhow!($$$ARGS))?"},
                    {"pattern": "$TRY.map_err(|$E| anyhow::anyhow!($$$ARGS))"},
                    {"pattern": "$TRY.map_err(|$E| anyhow!($$$ARGS))"},
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
