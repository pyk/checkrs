"""Lint: intermediate clone variables."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class IntermediateClones(Lint):
    """intermediate clone variables."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "intermediate_clones"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "intermediate clone variables"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "A variable is initialized with a `.clone()` and used in the"
            "immediate next statement."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "This suggests strict ownership flow issues. Consider: 1. If the"
            "original is not used later, move it instead of cloning. 2. If the"
            "clone is needed, inline it to `func(original.clone())` to avoid the"
            "intermediate variable noise."
        )

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "Note: In some cases clones are cheap and intentional; for example,"
            "cloning `Arc`/`Rc` is a cheap ref-count bump and may be acceptable."
            "If you use `Arc`/`Rc` intentionally, you can ignore or suppress this"
            "warning."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return "```rust\n// No example provided\n```"

    @property
    def help(self) -> str:
        """Return help text."""
        return "remove intermediate clone variables"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "all": [
                    {"kind": "block"},
                    {
                        "has": {
                            "all": [
                                {
                                    "any": [
                                        {"pattern": "let $VAR = $ORIG.clone();\n"},
                                        {
                                            "pattern": "let $VAR: $TYPE = "
                                            "$ORIG.clone();\n"
                                        },
                                    ]
                                },
                                {
                                    "precedes": {
                                        "pattern": "$FUNC($VAR);",
                                        "stopBy": "neighbor",
                                    }
                                },
                            ],
                            "stopBy": "end",
                        }
                    },
                    {
                        "not": {
                            "inside": {"pattern": "mod tests { $$$ }", "stopBy": "end"}
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
