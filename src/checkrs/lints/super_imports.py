"""Lint: super:: imports."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class SuperImports(Lint):
    """super:: imports."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "super_imports"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "super:: imports"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using super:: in use statements suggests poor module organization."
            "Consider restructuring your modules to use absolute paths or better"
            "module organization. Note: super:: is allowed inside test modules"
            "with #[cfg(test)]."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Using super:: in use statements suggests poor module organization."
            "Consider restructuring your modules to use absolute paths or better"
            "module organization. Note: super:: is allowed inside test modules"
            "with #[cfg(test)]."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "Using super:: in use statements suggests poor module organization."
            "Consider restructuring your modules to use absolute paths or better"
            "module organization. Note: super:: is allowed inside test modules"
            "with #[cfg(test)]."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n// No example provided\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "import items directly instead of using super::"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "use_declaration"},
                    {"regex": "\\buse\\s+super::"},
                    {
                        "not": {
                            "any": [
                                {
                                    "inside": {
                                        "pattern": "mod tests { $$$ }",
                                        "stopBy": "end",
                                    }
                                },
                                {
                                    "inside": {
                                        "kind": "mod_item",
                                        "follows": {
                                            "kind": "attribute_item",
                                            "regex": "#\\[cfg\\(test\\)\\]",
                                            "stopBy": "end",
                                        },
                                        "stopBy": "end",
                                    }
                                },
                            ]
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
