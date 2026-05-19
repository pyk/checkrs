"""Lint: path field types not using PathBuf."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class PathFieldTypes(Lint):
    """path field types not using PathBuf."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "path_field_types"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "path field types not using PathBuf"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Fields with names ending in `_path`, or named `path`/`paths`, should"
            "use `PathBuf` for proper path handling. This ensures cross-platform"
            "compatibility and allows using std::path utilities."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Instead of: ```rust pub struct Session { pub project_path: String, }```"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\npub struct Session {\n    pub project_path: String,\n}\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "use PathBuf for path-related struct fields"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "kind": "field_declaration",
                "all": [
                    {
                        "has": {
                            "kind": "field_identifier",
                            "regex": "_path$|^path$|^paths$|_dir$|^dir$|^dirs$",
                            "field": "name",
                        }
                    },
                    {"not": {"regex": "PathBuf"}},
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
