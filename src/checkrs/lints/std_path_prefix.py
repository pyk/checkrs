"""Lint: std::path::PathBuf fully-qualified paths."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class StdPathPrefix(Lint):
    """std::path::PathBuf fully-qualified paths."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "std_path_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return (
            "use a 'use std::path::PathBuf;' statement instead of the fully"
            "qualified path"
        )

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Use a 'use std::path::PathBuf;' statement instead of the fully"
            "qualified path"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Use a 'use std::path::PathBuf;' statement instead of the fully"
            "qualified path"
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
        return "import PathBuf instead of using the fully qualified path"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {"pattern": "std::path::PathBuf::$METHOD($$$ARGS)"},
                    {
                        "all": [
                            {"kind": "scoped_type_identifier"},
                            {"regex": "std::path::PathBuf"},
                        ]
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
