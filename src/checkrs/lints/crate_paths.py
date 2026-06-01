"""Lint: ban `crate::` usage outside of use declarations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class CratePaths(Lint):
    """Ban `crate::` usage outside of use declarations."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "crate_paths"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "crate:: paths outside of use declarations"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for `crate::` path prefixes outside of use declarations "
            "and reports them."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Using `crate::` outside of imports is verbose and breaks local "
            "consistency. Import items at the top of the module and use them "
            "directly."
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
            "// Bad\n"
            "fn setup() {\n"
            "    let x = crate::evm::chain::SetupInput::new(target);\n"
            "}\n"
            "\n"
            "// Good\n"
            "use crate::evm::chain::SetupInput;\n"
            "\n"
            "fn setup() {\n"
            "    let x = SetupInput::new(target);\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return (
            "if it is a struct, import `crate::module::MyStruct` and use "
            "`MyStruct` directly; if it is a free function, use its module "
            "directly (e.g. `crate::formatter::num` should be `formatter::num`)"
        )

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "all": [
                    {
                        "any": [
                            {"kind": "scoped_identifier", "regex": r"^crate::"},
                            {"kind": "scoped_type_identifier", "regex": r"^crate::"},
                        ]
                    },
                    {
                        "not": {
                            "inside": {
                                "kind": "use_declaration",
                                "stopBy": "end",
                            }
                        }
                    },
                    {
                        "not": {
                            "inside": {
                                "any": [
                                    {
                                        "kind": "scoped_identifier",
                                        "regex": r"^crate::",
                                    },
                                    {
                                        "kind": "scoped_type_identifier",
                                        "regex": r"^crate::",
                                    },
                                ],
                                "stopBy": "end",
                            }
                        }
                    },
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
