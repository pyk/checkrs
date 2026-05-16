"""Lint: match Option with bail! instead of with_context."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class AnyhowMatchOptionContext(Lint):
    """match Option with bail! instead of with_context."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_match_option_context"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "match Option with bail! instead of with_context"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return "When you have code like:"

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "```rust let contract_def = match selected_contract {"
            'Some(contract_def) => contract_def, None => bail!( "artifact {} does'
            'not contain contract definition {}", artifact.id, artifact.name ),'
            "}; ```"
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
            "let contract_def = match selected_contract {\n"
            "    Some(contract_def) => contract_def,\n"
            "    None => bail!(\n"
            '        "artifact {} does not contain contract definition {}",\n'
            "        artifact.id,\n"
            "        artifact.name\n"
            "    ),\n"
            "};\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use with_context on Option instead of match/bail!"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "any": [
                    {
                        "pattern": "match $OPT {\n"
                        "    Some($BIND) => $BIND,\n"
                        "    None => bail!($$$ARGS),\n"
                        "}\n"
                    },
                    {
                        "pattern": "match $OPT {\n"
                        "    Some($BIND) => $BIND,\n"
                        "    None => anyhow::bail!($$$ARGS),\n"
                        "}\n"
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
