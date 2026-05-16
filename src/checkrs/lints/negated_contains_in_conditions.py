"""Lint: negated contains() in conditions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class NegatedContainsInConditions(Lint):
    """negated contains() in conditions."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "negated_contains_in_conditions"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "negated contains() in conditions"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Negated contains() calls in if conditions are harder to read because"
            "you have to mentally invert the logic (not contains vs not exists)."
            "Extract the call to a named variable to make the intent self-"
            "documenting."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Instead of: if !available_list.contains(&crate_name) {}"

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
        return "extract negated contains() to a named variable"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "if_expression"},
                    {"pattern": "if !$EXPR.contains($$$ARGS) $BLOCK"},
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
