"""Lint: clone before serde_json::from_value."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class SerdeCloneIntoFromValue(Lint):
    """clone before serde_json::from_value."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "serde_clone_into_from_value"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "clone before serde_json::from_value"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "You are cloning a value immediately before passing it to"
            "serde_json::from_value(), which consumes ownership."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Review Data Flow:** Check if the original variable is used *after*"
            "this statement. If it is NOT used later: Remove `.clone()` and let"
            "ownership move into the function."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "Note: This rule cannot detect if the original variable is used"
            "later. Always verify data flow before applying the fix."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "// BAD: Unnecessary allocation\n"
            "let p = serde_json::from_value(data.clone());\n"
            "\n"
            "// GOOD: Move ownership instead\n"
            "let p = serde_json::from_value(data);\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "avoid cloning before serde_json::from_value"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {
                        "any": [
                            {"pattern": "serde_json::from_value($VAR.clone())"},
                            {
                                "pattern": (
                                    "serde_json::from_value::<$TYPE>($VAR.clone())"
                                ),
                            },
                        ]
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
