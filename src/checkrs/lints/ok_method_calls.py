"""Lint: ok() method calls."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class OkMethodCalls(Lint):
    """ok() method calls."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "ok_method_calls"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "ok() method calls"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Prefer using the `?` operator to propagate errors, or explicitly"
            "handle the error with `match`/`if let` instead of silently"
            "converting to None."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "For test code, using .ok() may be acceptable, but consider more"
            "explicit error handling even in tests."
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
        return "propagate errors with `?` instead of ok()"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"pattern": "$EXPR.ok()"},
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
                                            "regex": "#[\\[]*test",
                                            "stopBy": "end",
                                        },
                                        "stopBy": "end",
                                    }
                                },
                                {
                                    "follows": {
                                        "kind": "attribute_item",
                                        "regex": "#[\\[]*test",
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
