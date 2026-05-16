"""Lint: let chains in if let."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class LetChainsInIfLet(Lint):
    """let chains in if let."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "let_chains_in_if_let"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "let chains in if let"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "if-let statements combine pattern matching with control flow in a"
            "way that can be hard to follow. Prefer using match expressions for"
            "explicit pattern matching."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "# Before"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "NOTE: `bail!` is used for binary only, for a library you should"
            "returns Error."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "if let Some(parent) = md_path.parent()\n"
            "    && !parent.exists()\n"
            "{\n"
            "    std::fs::create_dir_all(parent)?;\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use match expressions instead of let chains in if let"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {
                        "any": [
                            {"pattern": "if let $PAT = $EXPR { $$$ }"},
                            {"kind": "let_chain"},
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
