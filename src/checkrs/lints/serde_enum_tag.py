"""Lint: enums without serde(tag) or serde(untagged)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


class SerdeEnumTag(Lint):
    """enums without serde(tag) or serde(untagged)."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "serde_enum_tag"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "enums without serde(tag) or serde(untagged)"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Enums that derive `Deserialize` without a proper serde tagging"
            "attribute can lead to unexpected deserialization issues."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Consider adding one of the following attributes:"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return "None."

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "#[derive(Debug, PartialEq, Clone, Deserialize)]\n"
            '#[serde(tag = "type")]\n'
            "pub enum Model {\n"
            "    // variants\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "add serde(tag) or serde(untagged) to enums with Deserialize"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(
            rule={
                "kind": "enum_item",
                "follows": {
                    "stopBy": "end",
                    "kind": "attribute_item",
                    "has": {
                        "kind": "attribute",
                        "all": [
                            {"has": {"kind": "identifier", "regex": "^derive$"}},
                            {"has": {"kind": "token_tree", "regex": "Deserialize"}},
                        ],
                    },
                },
                "not": {
                    "follows": {
                        "stopBy": "end",
                        "kind": "attribute_item",
                        "has": {
                            "kind": "attribute",
                            "all": [
                                {"has": {"kind": "identifier", "regex": "^serde$"}},
                                {
                                    "any": [
                                        {
                                            "has": {
                                                "kind": "token_tree",
                                                "regex": "untagged",
                                            }
                                        },
                                        {
                                            "has": {
                                                "kind": "token_tree",
                                                "regex": "tag\\s*=",
                                            }
                                        },
                                    ]
                                },
                            ],
                        },
                    }
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
