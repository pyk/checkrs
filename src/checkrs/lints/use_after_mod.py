"""Lint: use declarations after mod declarations."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class UseAfterMod(Lint):
    """use declarations after mod declarations."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "use_after_mod"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "use declarations after mod declarations"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "use statements should appear before mod declarations"

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "use statements should appear before mod declarations"

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
        return "place use declarations before mod declarations"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "kind": "use_declaration",
                "inside": {"kind": "source_file"},
                "follows": {"kind": "mod_item", "stopBy": "end"},
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
