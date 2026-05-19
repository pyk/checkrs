"""Lint: <one-line description>."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class <ClassName>(Lint):
    """<Short description of what this lint checks>."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "<lint_name>"

    @property
    def description(self) -> str:
        """Return the lint description.

        Must be short and read well with a count prefix:
        "3 <description>". Keep it under 8 words.
        """
        return "<short phrase that fits after a count>"

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

    @property
    def help(self) -> str:
        """Return a short rule or fix sentence.

        Printed once after all file locations.
        """
        return "<one sentence explaining the rule or fix>"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a single file and return any violations."""
        # Example: match a specific pattern
        # config = make_config(
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
        #             message="missing",
        #         ),
        #     )
        # return violations

        return []
