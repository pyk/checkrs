"""Lint: String parameter ownership."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class OwnedStringParameters(Lint):
    """String parameter ownership."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "owned_string_parameters"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "String parameter ownership"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Taking ownership of String parameters is often unnecessary. Using"
            "&str is more flexible:"
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "- Allows passing both String and &str literals - More efficient when"
            "ownership isn't needed - Reduces unnecessary cloning"
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
            "fn show(item_path: String) -> Result<()> {\n"
            '    debug!("Show command: item_path={}", item_path);\n'
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "accept &str instead of String when ownership is not needed"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "parameter"},
                    {"has": {"kind": "type_identifier", "regex": "^String$"}},
                    {"not": {"inside": {"kind": "generic_type"}}},
                    {
                        "not": {
                            "inside": {"matches": "isFromStringImpl", "stopBy": "end"}
                        }
                    },
                ]
            },
            utils={"isFromStringImpl": {"pattern": "impl From<String> for $TYPE"}},
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
