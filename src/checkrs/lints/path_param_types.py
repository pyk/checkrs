"""Lint: path parameter types not using impl AsRef<Path>."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class PathParamTypes(Lint):
    """path parameter types not using impl AsRef<Path>."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "path_param_types"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "path parameter types not using impl AsRef<Path>"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Parameters with names ending in `_path` or `_dir`, or named"
            "`path`/`paths`/`dir`/`dirs`, should use `impl AsRef<Path>` for"
            "maximum flexibility. This allows callers to pass any type that can"
            "be converted to a path reference."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Instead of: ```rust pub fn new(session_id: u64, project_path: &str,"
            "model: &str) -> Self { // ... } ```"
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
            "pub fn new(session_id: u64, project_path: &str, model: &str) -> Self {\n"
            "    // ...\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use impl AsRef<Path> for path-related parameters"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "kind": "parameter",
                "all": [
                    {
                        "has": {
                            "kind": "identifier",
                            "regex": "_path$|_dir$|^path$|^dir$|^paths$|^dirs$",
                            "field": "pattern",
                        }
                    },
                    {
                        "not": {
                            "has": {
                                "kind": "identifier",
                                "regex": "^json_path$",
                                "field": "pattern",
                            }
                        }
                    },
                    {"not": {"all": [{"regex": "Option<"}, {"regex": "Path"}]}},
                    {"not": {"regex": "AsRef<Path>"}},
                ],
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
