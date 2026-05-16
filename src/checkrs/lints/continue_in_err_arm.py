"""Lint: continue inside Err match arms."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class ContinueInErrArm(Lint):
    """continue inside Err match arms."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "continue_in_err_arm"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "continue inside Err match arms"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "Using `continue` inside an Err arm makes control flow hard to follow."

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Problem:** The code mixes error handling with loop control flow in"
            "a way that is difficult to reason about."
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
        return "refactor continue in Err arms to let-else"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "continue_expression"},
                    {
                        "inside": {
                            "stopBy": "end",
                            "kind": "match_arm",
                            "has": {
                                "kind": "match_pattern",
                                "has": {
                                    "any": [
                                        {"kind": "identifier", "regex": "^Err$"},
                                        {
                                            "kind": "tuple_struct_pattern",
                                            "has": {
                                                "kind": "identifier",
                                                "regex": "^Err$",
                                            },
                                        },
                                        {
                                            "kind": "tuple_struct_pattern",
                                            "has": {
                                                "kind": "scoped_identifier",
                                                "regex": "::Err$",
                                            },
                                        },
                                        {
                                            "kind": "tuple_struct_pattern",
                                            "has": {
                                                "kind": "tuple_struct_pattern",
                                                "has": {
                                                    "kind": "scoped_identifier",
                                                    "regex": "::Err$",
                                                },
                                            },
                                        },
                                    ]
                                },
                            },
                        }
                    },
                    {"not": {"inside": {"kind": "match_expression"}}},
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
