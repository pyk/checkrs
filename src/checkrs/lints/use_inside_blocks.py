"""Lint: use declarations inside blocks."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class UseInsideBlocks(Lint):
    """use declarations inside blocks."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "use_inside_blocks"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "use declarations inside blocks"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "Move import statements to module level for better organization."

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Incorrect:** ```rust match args.command { Commands::Acp => { use"
            'tracing::info; info!("test"); } } ```'
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
            "match args.command {\n"
            "    Commands::Acp => {\n"
            "        use tracing::info;\n"
            '        info!("test");\n'
            "    }\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "place use declarations at the top of the module"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "kind": "use_declaration",
                "inside": {"kind": "block", "stopBy": "end"},
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
