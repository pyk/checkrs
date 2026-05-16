"""Lint: ok_or_else with anyhow! instead of context()."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class AnyhowPreferContext(Lint):
    """ok_or_else with anyhow! instead of context()."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_prefer_context"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "ok_or_else with anyhow! instead of context()"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using `.context()` is more concise and idiomatic than `.ok_or_else`"
            "with `anyhow!` macro."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Instead of: ```rust let dest_path = path_mappings .output_map"
            '.get(&dep.absolute_path) .ok_or_else(|| anyhow::anyhow!( "Missing'
            'output path for dependency {} in path_mappings",'
            "dep.absolute_path.display() ))?; ```"
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "Note: .context() doesn't support format arguments, so you may need"
            "to simplify the message."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "let dest_path = path_mappings\n"
            "    .output_map\n"
            "    .get(&dep.absolute_path)\n"
            "    .ok_or_else(|| anyhow::anyhow!(\n"
            '        "Missing output path for dependency {} in path_mappings",\n'
            "        dep.absolute_path.display()\n"
            "    ))?;\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use context() instead of ok_or_else with anyhow!"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {"pattern": "$_EXPR.ok_or_else(|| anyhow::anyhow!($$$ARGS))?"},
                    {"pattern": "$_EXPR.ok_or_else(|| anyhow!($$$ARGS))?"},
                    {"pattern": "$_EXPR.ok_or_else(|| anyhow::anyhow!($$$ARGS))"},
                    {"pattern": "$_EXPR.ok_or_else(|| anyhow!($$$ARGS))"},
                    {"pattern": "$_EXPR.ok_or_else(|| { anyhow::anyhow!($$$ARGS) })?"},
                    {"pattern": "$_EXPR.ok_or_else(|| { anyhow!($$$ARGS) })?"},
                    {"pattern": "$_EXPR.ok_or_else(|| { anyhow::anyhow!($$$ARGS) })"},
                    {"pattern": "$_EXPR.ok_or_else(|| { anyhow!($$$ARGS) })"},
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
