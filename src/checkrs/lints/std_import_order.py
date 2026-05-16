"""Lint: std imports not on top."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class StdImportOrder(Lint):
    """std imports not on top."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "std_import_order"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "std imports not on top"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "**Incorrect:** ```rust use anyhow::Result; use clap::Parser; use"
            "std::path::PathBuf; ```"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "**Correct:** ```rust use std::path::PathBuf;"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "use anyhow::Result;\n"
            "use clap::Parser;\n"
            "use std::path::PathBuf;\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "place std imports before external and crate imports"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "kind": "use_declaration",
                "regex": "^use std::",
                "follows": {
                    "all": [
                        {"kind": "use_declaration"},
                        {"not": {"regex": "^use std::"}},
                    ],
                    "stopBy": "end",
                },
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
