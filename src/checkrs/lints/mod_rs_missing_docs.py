"""Lint: mod.rs files must have module-level documentation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class ModRsMissingDocs(Lint):
    """Checks that mod.rs files contain a module doc comment."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "mod_rs_missing_docs"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "mod.rs files missing `//!` module doc"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks whether `mod.rs` files start with a module doc comment (``//!``)."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Module documentation helps readers understand the purpose of a module "
            "immediately. A `mod.rs` without docs forces developers to read the code "
            "to infer intent. The style should be simple, not abstract, and direct."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n//! This module handles user authentication.\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "module docs must be simple, not abstract, and direct"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check whether the file has module-level documentation."""
        if file_path.name != "mod.rs":
            return []


        config = make_config(
            rule={
                "kind": "source_file",
                "has": {
                    "kind": "line_comment",
                    "regex": r"^//!\s*\S",
                },
            },
        )
        matches = list(node.find_all(config))

        if matches:
            return []

        return [
            Violation(
                lint_name=self.name,
                file_path=file_path,
                line=1,
                column=1,
                message="missing",
            ),
        ]
