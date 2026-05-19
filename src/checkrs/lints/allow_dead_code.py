"""Lint: using #[allow(dead_code)] attribute."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AllowDeadCode(Lint):
    """using #[allow(dead_code)] attribute."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "allow_dead_code"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "using #[allow(dead_code)] attribute"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Remove unused code instead of suppressing this error. Suppressing"
            "dead_code warnings reduces code quality and maintainability."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Remove unused code instead of suppressing this error. Suppressing"
            "dead_code warnings reduces code quality and maintainability."
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
        return "remove allow(dead_code) and refactor unused code"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "attribute"},
                    {"has": {"kind": "identifier", "regex": "^allow$"}},
                    {
                        "has": {
                            "kind": "token_tree",
                            "field": "arguments",
                            "has": {"kind": "identifier", "regex": "^dead_code$"},
                        }
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
