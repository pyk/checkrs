"""Lint: clap::Subcommand fully-qualified paths."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class ClapSubcommandPrefix(Lint):
    """clap::Subcommand fully-qualified paths."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "clap_subcommand_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "clap::Subcommand fully-qualified paths"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Prefer importing `clap::Subcommand` at the top of the file and using"
            "`Subcommand` directly."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Bad: #[derive(clap::Subcommand)] enum Commands {}"

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
        return "import Subcommand instead of using the fully qualified path"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={"all": [{"kind": "attribute_item"}, {"regex": "clap::Subcommand"}]},
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
