"""Lint: inconsistent example headers."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class InconsistentExampleHeaders(Lint):
    """inconsistent example headers."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "inconsistent_example_headers"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "inconsistent example headers"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Use '# Example' as the standard header for code examples in"
            "documentation. This provides a consistent naming convention across"
            "all doc comments."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Use '# Example' as the standard header for code examples in"
            "documentation. This provides a consistent naming convention across"
            "all doc comments."
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
        return "use '# Example' consistently"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "line_comment"},
                    {"regex": "///\\s*#\\s*Example Usage"},
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
