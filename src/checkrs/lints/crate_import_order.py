"""Lint: crate imports before external imports."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class CrateImportOrder(Lint):
    """crate imports before external imports."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "crate_import_order"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "crate imports before external imports"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "**Incorrect:** ```rust use crate::acp::types::{AgentCapabilities,"
            "InitializeRequest}; use anyhow::Result; use tracing::{info, warn};"
            "```"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "**Correct:** ```rust use anyhow::Result; use tracing::{info, warn};"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "use crate::acp::types::{AgentCapabilities, InitializeRequest};\n"
            "use anyhow::Result;\n"
            "use tracing::{info, warn};\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "place crate imports after external imports"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "kind": "use_declaration",
                "regex": "^use crate::",
                "precedes": {
                    "all": [
                        {"kind": "use_declaration"},
                        {
                            "not": {
                                "any": [
                                    {"regex": "^use std::"},
                                    {"regex": "^use crate::"},
                                    {"regex": "^use self::"},
                                    {"regex": "^use super::"},
                                ]
                            }
                        },
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
