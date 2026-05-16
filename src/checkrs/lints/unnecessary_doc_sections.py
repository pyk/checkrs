"""Lint: unnecessary doc comment sections."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class UnnecessaryDocSections(Lint):
    """unnecessary doc comment sections."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "unnecessary_doc_sections"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "unnecessary doc comment sections"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Types and return values are already documented in the function"
            "signature. Do not duplicate this information in doc comments. Only"
            "use allowed section headers in documentation (Example, Examples)."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Types and return values are already documented in the function"
            "signature. Do not duplicate this information in doc comments. Only"
            "use allowed section headers in documentation (Example, Examples)."
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
        return "remove non-idiomatic doc comment sections"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "line_comment"},
                    {
                        "regex": "(///|//!)\\s*#\\s*(Design "
                        "Philosophy|Arguments|Parameters|Returns|Errors|Panics|Safety|E"
                        "xample "
                        "Usage)(?:\\s|$)"
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
