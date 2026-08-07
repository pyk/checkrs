"""Lint: enums without serde(tag) or serde(untagged)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


# Only walk contiguous preceding attributes/comments for this item.
# stopBy: end incorrectly matches attributes from earlier sibling items.
_ATTR_STOP_BY = {
    "not": {
        "any": [
            {"kind": "attribute_item"},
            {"kind": "line_comment"},
            {"kind": "block_comment"},
        ]
    }
}


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
            "Non-unit enums that derive `Deserialize` without `serde(tag)` or"
            " `serde(untagged)` use externally tagged representation, which can"
            " lead to unexpected deserialization issues."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return "Consider adding one of the following attributes:"

    @property
    def known_issues(self) -> str:
        """Return known issues."""
        return (
            "Unit-only enums (string enums) are exempt because default"
            " externally tagged unit variants serialize as plain strings."
            " Attributes inside `cfg_attr` are not detected."
        )

    @property
    def example(self) -> str:
        """Return example code."""
        return (
            "```rust\n"
            "#[derive(Debug, PartialEq, Clone, Deserialize)]\n"
            '#[serde(tag = "type")]\n'
            "pub enum Model {\n"
            "    Named { name: String },\n"
            "    Custom(String),\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "add serde(tag) or serde(untagged) to enums with Deserialize"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {"kind": "enum_item"},
                    {
                        "follows": {
                            "stopBy": _ATTR_STOP_BY,
                            "kind": "attribute_item",
                            "has": {
                                "kind": "attribute",
                                "all": [
                                    {
                                        "has": {
                                            "kind": "identifier",
                                            "regex": "^derive$",
                                        }
                                    },
                                    {
                                        "has": {
                                            "kind": "token_tree",
                                            "regex": "Deserialize",
                                        }
                                    },
                                ],
                            },
                        },
                    },
                    {
                        "not": {
                            "follows": {
                                "stopBy": _ATTR_STOP_BY,
                                "kind": "attribute_item",
                                "has": {
                                    "kind": "attribute",
                                    "all": [
                                        {
                                            "has": {
                                                "kind": "identifier",
                                                "regex": "^serde$",
                                            }
                                        },
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
                        }
                    },
                    # Unit-only enums intentionally use plain string encoding.
                    {
                        "any": [
                            {
                                "has": {
                                    "stopBy": "end",
                                    "kind": "field_declaration_list",
                                }
                            },
                            {
                                "has": {
                                    "stopBy": "end",
                                    "kind": "ordered_field_declaration_list",
                                }
                            },
                        ]
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
