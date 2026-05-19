"""Lint: is_some() followed by bail! in if blocks."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AnyhowIsSomeBail(Lint):
    """is_some() followed by bail! in if blocks."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_is_some_bail"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "is_some() followed by bail! in if blocks"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using `ensure!` with `is_none()` is more concise and readable than"
            "checking `is_some()` with a `bail!` in an if statement."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Incorrect:** ```rust if entries.next().is_some() {"
            "anyhow::bail!(\"Path '{}' is not empty\", path.display()); } ```"
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
            "if entries.next().is_some() {\n"
            "    anyhow::bail!(\"Path '{}' is not empty\", path.display());\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use ensure! with is_none() instead of if/is_some/bail!"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {"pattern": "if $EXPR.is_some() { bail!($$$ARGS); }"},
                    {"pattern": "if $EXPR.is_some() { anyhow::bail!($$$ARGS); }"},
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
