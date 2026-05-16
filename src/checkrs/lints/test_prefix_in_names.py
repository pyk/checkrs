"""Lint: test_ prefix in test names."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class TestPrefixInNames(Lint):
    """test_ prefix in test names."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "test_prefix_in_names"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "test_ prefix in test names"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Instead of `test_builder_minimal_fields`, name it"
            "`builder_minimal_fields` or"
            "`builder_creates_request_with_minimal_fields` to describe what is"
            "being tested."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Instead of `test_builder_minimal_fields`, name it"
            "`builder_minimal_fields` or"
            "`builder_creates_request_with_minimal_fields` to describe what is"
            "being tested."
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
        return "remove test_ prefix from test function names"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "function_item"},
                    {"follows": {"pattern": "#[test]"}},
                    {"has": {"kind": "identifier", "regex": "^test_", "field": "name"}},
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
