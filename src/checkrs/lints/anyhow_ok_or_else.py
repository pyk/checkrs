"""Lint: ok_or_else with anyhow macros."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AnyhowOkOrElse(Lint):
    """ok_or_else with anyhow macros."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_ok_or_else"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "ok_or_else with anyhow macros"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using `bail!` is more concise and readable than `ok_or_else` with`anyhow`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Instead of: ```rust let result = option.ok_or_else(||"
            'anyhow::anyhow!("message"))?; ```'
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
            'let result = option.ok_or_else(|| anyhow::anyhow!("message"))?;\n'
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "avoid ok_or_else with anyhow macros"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {"pattern": "$OPT.ok_or_else(|| anyhow::anyhow!($$$ARGS))?"},
                    {"pattern": "$OPT.ok_or_else(|| anyhow!($$$ARGS))?"},
                    {"pattern": "$OPT.ok_or_else(|| anyhow::anyhow!($$$ARGS))"},
                    {"pattern": "$OPT.ok_or_else(|| anyhow!($$$ARGS))"},
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
