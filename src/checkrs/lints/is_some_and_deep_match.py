"""Lint: deep matching with is_some_and()."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class IsSomeAndDeepMatch(Lint):
    """deep matching with is_some_and()."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "is_some_and_deep_match"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "deep matching with is_some_and()"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Combining extraction and validation in `.is_some_and()` makes code"
            "harder to debug. Prefer separating into explicit steps: first"
            "unwrap/extract, then validate in a separate if/match statement."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "# Before ```rust if attr.path().segments.last().is_some_and(|seg|"
            'seg.ident == "method") { // process } ```'
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
            'if attr.path().segments.last().is_some_and(|seg| seg.ident == "method")'
            "{\n"
            "    // process\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "separate extraction and validation from is_some_and()"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"pattern": "$EXPR.is_some_and($CLOSURE)"},
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
