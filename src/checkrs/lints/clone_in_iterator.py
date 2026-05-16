"""Lint: clone() inside iterators."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class CloneInIterator(Lint):
    """clone() inside iterators."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "clone_in_iterator"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "clone() inside iterators"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "The .map() iterator method executes its closure for each element."
            "Cloning inside the closure incurs the cost for every iteration."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Consider these alternatives: 1. Use references (&T) instead of"
            "cloning when possible 2. Restructure code to clone outside the"
            "iterator chain 3. Use .cloned() for Clone types instead of manual"
            "cloning in closure 4. Use iterator adaptors that avoid cloning"
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
            "let result: Vec<_> = items.iter().map(|item| item.clone()).collect();\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "avoid cloning inside iterator methods"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "closure_expression"},
                    {"has": {"stopBy": "end", "pattern": "$VAR.clone()"}},
                    {"inside": {"stopBy": "end", "pattern": "$X.map($$$)"}},
                    {
                        "not": {
                            "has": {
                                "stopBy": "end",
                                "regex": "(?i)\\w*(arc|rc)\\w*\\.clone\\(\\)",
                            }
                        }
                    },
                    {
                        "not": {
                            "inside": {"pattern": "mod tests { $$$ }", "stopBy": "end"}
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
