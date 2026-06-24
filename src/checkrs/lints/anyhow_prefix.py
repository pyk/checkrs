"""Lint: anyhow::bail!/ensure! macro with prefix."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AnyhowPrefix(Lint):
    """anyhow::bail!/ensure! macro with prefix."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "anyhow::bail!/ensure! macro with prefix"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Import the `bail!` or `ensure!` macro once at the top of the file and use"
            " it without the `anyhow::` prefix for cleaner, more idiomatic code."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Incorrect:** ```rust let Some(choice) ="
            'chat_response.choices.first() else { anyhow::bail!("No choices in'
            'response"); };'
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
            "let Some(choice) = chat_response.choices.first() else {\n"
            '    anyhow::bail!("No choices in response");\n'
            "};\n"
            "\n"
            "let Some(content) = &choice.message.content else {\n"
            '    anyhow::bail!("No content in response");\n'
            "};\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "import bail!/ensure! and use without the anyhow:: prefix"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {"pattern": "anyhow::bail!($$$ARGS)"},
                    {"pattern": "anyhow::ensure!($$$ARGS)"},
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
