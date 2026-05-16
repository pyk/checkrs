"""Lint: match expressions with panic catch-all arms."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ast_grep_py

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path


_RULE = {
    "all": [
        {"kind": "match_expression"},
        {
            "any": [
                {
                    "all": [
                        {
                            "has": {
                                "kind": "match_block",
                                "nthChild": 2,
                                "has": {
                                    "kind": "match_arm",
                                    "nthChild": 1,
                                    "not": {
                                        "has": {
                                            "kind": "match_pattern",
                                            "regex": "^_$",
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "has": {
                                "kind": "match_block",
                                "nthChild": 2,
                                "has": {
                                    "kind": "match_arm",
                                    "nthChild": 2,
                                    "all": [
                                        {
                                            "has": {
                                                "kind": "match_pattern",
                                                "regex": "^_$",
                                            }
                                        },
                                        {
                                            "has": {
                                                "kind": "block",
                                                "has": {
                                                    "kind": "macro_invocation",
                                                    "has": {
                                                        "kind": "identifier",
                                                        "regex": "^panic$",
                                                    },
                                                },
                                            }
                                        },
                                    ],
                                },
                            }
                        },
                    ]
                },
                {
                    "all": [
                        {
                            "has": {
                                "kind": "match_block",
                                "nthChild": 2,
                                "has": {
                                    "kind": "match_arm",
                                    "nthChild": 1,
                                    "not": {
                                        "has": {
                                            "kind": "match_pattern",
                                            "regex": "^_$",
                                        }
                                    },
                                },
                            }
                        },
                        {
                            "has": {
                                "kind": "match_block",
                                "nthChild": 2,
                                "has": {
                                    "kind": "match_arm",
                                    "nthChild": 2,
                                    "all": [
                                        {
                                            "has": {
                                                "kind": "match_pattern",
                                                "regex": "^_$",
                                            }
                                        },
                                        {
                                            "has": {
                                                "kind": "macro_invocation",
                                                "has": {
                                                    "kind": "identifier",
                                                    "regex": "^panic$",
                                                },
                                            }
                                        },
                                    ],
                                },
                            }
                        },
                    ]
                },
            ]
        },
    ]
}


class MatchPanicToLetElse(Lint):
    """match expressions with panic catch-all arms."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "match_panic_to_let_else"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "match expressions with panic catch-all arms"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "This match expression with a single specific arm and a catch-all"
            "panic arm can be simplified to a let-else pattern."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "**Before:** ```rust match value { Pattern(v) => { /* handle */ } _"
            '=> panic!("expected Pattern"), } ```'
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
            "match value {\n"
            "    Pattern(v) => { /* handle */ }\n"
            '    _ => panic!("expected Pattern"),\n'
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "refactor match with panic catch-all to let-else"

    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a file and return any violations."""
        root = ast_grep_py.SgRoot(source, "rust")
        node = root.root()

        config = make_config(rule=_RULE)

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
