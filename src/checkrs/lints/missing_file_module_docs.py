"""Lint: files missing `//!` module doc."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class MissingFileModuleDocs(Lint):
    """files missing `//!` module doc."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "missing_file_module_docs"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "files missing `//!` module doc"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "Add module-level documentation using `//!` at the top of the file."

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Basic examples (for modules inside binary):"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "//! Centralized error types for cargo-txt.\n"
            "//!\n"
            "//! This module defines all error types used throughout the application,\n"
            "//! providing consistent error handling and user-friendly error"
            "messages.\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "add module-level documentation using `//!`"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "source_file"},
                    {
                        "has": {
                            "any": [
                                {"kind": "function_item"},
                                {"kind": "struct_item"},
                                {"kind": "enum_item"},
                                {"kind": "impl_item"},
                                {"kind": "mod_item"},
                                {"kind": "trait_item"},
                                {"kind": "use_declaration"},
                            ]
                        }
                    },
                    {
                        "not": {
                            "has": {
                                "kind": "line_comment",
                                "has": {"kind": "inner_doc_comment_marker"},
                            }
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
