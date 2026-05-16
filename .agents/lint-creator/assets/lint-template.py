"""Lint: <one-line description>."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation

if TYPE_CHECKING:
    from pathlib import Path


class <ClassName>(Lint):
    """<Short description of what this lint checks>."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "<lint_name>"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "<one-line summary>"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "<detailed explanation>"

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "<explanation>"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "<example code>\n"
            "```"
        )

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a single file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        # Example: match a specific pattern
        # config = ast_grep_py.Config(
        #     rule={
        #         "kind": "<ast_kind>",
        #         "pattern": "$A",
        #     },
        # )
        # matches = list(node.find_all(config))

        # Example: iterate matches and build violations
        # violations: list[Violation] = []
        # for m in matches:
        #     r = m.range()
        #     violations.append(
        #         Violation(
        #             lint_name=self.name,
        #             file_path=file_path,
        #             line=r.start.line,
        #             column=r.start.column,
        #             message="<violation message>",
        #         ),
        #     )
        # return violations

        return []
