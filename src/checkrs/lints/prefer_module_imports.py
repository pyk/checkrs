"""Lint: item imports from crate modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class PreferModuleImports(Lint):
    """item imports from crate modules."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "prefer_module_imports"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "item imports from crate modules"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Import the module instead of specific items. Use 'use"
            "crate::module;' and reference items as module::item"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Import the module instead of specific items. Use 'use"
            "crate::module;' and reference items as module::item"
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
        return "import the module instead of specific items"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={"kind": "use_declaration", "pattern": "use $ARG;"},
            constraints={
                "ARG": {
                    "any": [
                        {
                            "all": [
                                {"kind": "scoped_identifier"},
                                {"regex": "crate::.+::[A-Z]"},
                            ]
                        },
                        {
                            "all": [
                                {"kind": "scoped_use_list"},
                                {
                                    "has": {
                                        "kind": "scoped_identifier",
                                        "regex": "crate::",
                                    }
                                },
                            ]
                        },
                    ]
                }
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
