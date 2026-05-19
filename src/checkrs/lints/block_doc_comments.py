"""Lint: block-style doc comments."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class BlockDocComments(Lint):
    """block-style doc comments."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "block_doc_comments"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "block-style doc comments"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Block-style doc comments (starting with `/**` or `/*!`) are not"
            "idiomatic for module-level documentation in Rust and can be"
            "confusing. Prefer using line-style doc comments:"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "- Use `//!` for module-level (inner) documentation that applies to"
            "the whole file. - Use `///` for item-level (outer) documentation"
            "that documents the following item."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "/**\n"
            " * Orchestrator-only contract module for the scan command.\n"
            " *\n"
            " * Responsibilities:\n"
            " *  - Build contract-level model from an Artifact (name, natspec, storage"
            "layout).\n"
            " *  - Delegate action extraction and rendering to `contract_action`"
            "module.\n"
            " */\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "replace block doc comments with line doc comments"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={"all": [{"kind": "block_comment"}, {"regex": "^/[*][*]|^/[*]!"}]},
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
