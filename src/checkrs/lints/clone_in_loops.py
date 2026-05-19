"""Lint: clone() inside loops."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class CloneInLoops(Lint):
    """clone() inside loops."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "clone_in_loops"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "clone() inside loops"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Consider these alternatives: 1. Lift the clone out of the loop if"
            "the value is invariant 2. Use references (&T) instead of ownership"
            "when possible 3. Use .collect() on iterators instead of manual"
            "pushing of clones 4. Use Cow (Clone-on-Write) for conditional"
            "cloning"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Arc/Rc clones are excluded since they only increment a referencecounter."
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
        return "avoid cloning inside loops"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {
                        "any": [
                            {"inside": {"kind": "for_expression", "stopBy": "end"}},
                            {"inside": {"kind": "while_expression", "stopBy": "end"}},
                            {"inside": {"kind": "loop_expression", "stopBy": "end"}},
                        ]
                    },
                    {"pattern": "$VAR.clone()"},
                    {
                        "not": {
                            "any": [
                                {
                                    "inside": {
                                        "pattern": "mod tests { $$$ }",
                                        "stopBy": "end",
                                    }
                                },
                                {"regex": "(?i)\\w*(arc|rc)\\w*\\.clone\\(\\)"},
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
