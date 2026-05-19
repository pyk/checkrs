"""Lint: nested if let expressions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class NestedIfLet(Lint):
    """nested if let expressions."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "nested_if_let"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "nested if let expressions"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Nested `if let` expressions create non-linear control flow that is"
            "hard to read. Consider these alternatives:"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "1. Use `match` for complex pattern matching:"

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
        return "use match or and_then instead of nested if let"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"pattern": "if let $PAT = $EXPR { $$$ }"},
                    {
                        "has": {
                            "field": "consequence",
                            "has": {"kind": "if_expression", "stopBy": "end"},
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
