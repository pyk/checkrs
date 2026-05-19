"""Lint: if let blocks with more than 5 statements."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class LongIfLetBlocks(Lint):
    """if let blocks with more than 5 statements."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "long_if_let_blocks"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "if let blocks with more than 5 statements"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Long `if let` blocks with many statements are hard to read and"
            "maintain. Consider refactoring the logic into a separate function or"
            "using a different control flow structure."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Long `if let` blocks with many statements are hard to read and"
            "maintain. Consider refactoring the logic into a separate function or"
            "using a different control flow structure."
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
        return "refactor if let blocks longer than 5 statements"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "if_expression"},
                    {"has": {"field": "condition", "kind": "let_condition"}},
                    {
                        "has": {
                            "field": "consequence",
                            "kind": "block",
                            "has": {"nthChild": 6},
                        }
                    },
                    {
                        "not": {
                            "has": {
                                "any": [
                                    {"pattern": "return $$$"},
                                    {"pattern": "break"},
                                    {"pattern": "break $$$"},
                                    {"pattern": "continue"},
                                    {"pattern": "$PATH::exit($$$)"},
                                ],
                                "stopBy": "end",
                            }
                        }
                    },
                    {
                        "not": {
                            "any": [
                                {
                                    "inside": {
                                        "pattern": "mod tests { $$$ }",
                                        "stopBy": "end",
                                    }
                                },
                                {
                                    "inside": {
                                        "kind": "function_item",
                                        "follows": {
                                            "kind": "attribute_item",
                                            "regex": "test",
                                            "stopBy": "end",
                                        },
                                        "stopBy": "end",
                                    }
                                },
                                {
                                    "follows": {
                                        "kind": "attribute_item",
                                        "regex": "test",
                                        "stopBy": "end",
                                    }
                                },
                            ]
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
