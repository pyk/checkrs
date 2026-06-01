"""Lint: ban `crate::` usage inside function bodies."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class CrateInFunctions(Lint):
    """Ban `crate::` usage inside function bodies."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "crate_in_functions"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "crate:: paths inside function bodies"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for `crate::` path prefixes inside function bodies and "
            "reports them."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Using `crate::` inside functions is verbose and breaks local "
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
                    {"kind": "scoped_identifier", "regex": r"^crate::"},
                    {"inside": {"kind": "block", "stopBy": "end"}},
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
                                "kind": "scoped_identifier",
                                "regex": r"^crate::",
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
