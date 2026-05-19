"""Lint: turbofish syntax with collect()."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class TurbofishCollect(Lint):
    """turbofish syntax with collect()."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "turbofish_collect"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "turbofish syntax with collect()"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using type annotations on the let binding is more readable than"
            "turbofish syntax."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Instead of: ```rust let text = element.text().collect::<String>();```"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\nlet text = element.text().collect::<String>();\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "use a type annotation instead of turbofish with collect()"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"pattern": "let $VAR = $EXPR.collect::<$TYPE>();"},
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
