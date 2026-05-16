"""Lint: non-test module declarations."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class NonTestModuleDeclarations(Lint):
    """non-test module declarations."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "non_test_module_declarations"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "non-test module declarations"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Follow Rust's module organization: - If the module is simple, use"
            "one file without creating submodules - If the module is complex,"
            "create the module in a separate file (module_name.rs or"
            "module_name/mod.rs)"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Follow Rust's module organization: - If the module is simple, use"
            "one file without creating submodules - If the module is complex,"
            "create the module in a separate file (module_name.rs or"
            "module_name/mod.rs)"
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
        return "move non-test modules to separate files"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "mod_item"},
                    {"has": {"kind": "declaration_list", "field": "body"}},
                    {"not": {"inside": {"kind": "mod_item"}}},
                    {"not": {"has": {"kind": "identifier", "regex": "^tests$"}}},
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
