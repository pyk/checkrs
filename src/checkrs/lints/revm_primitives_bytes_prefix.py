"""Lint: import Bytes instead of using the fully qualified path."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class RevmPrimitivesBytesPrefix(Lint):
    """revm::primitives::Bytes fully-qualified paths."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "revm_primitives_bytes_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "revm::primitives::Bytes used with fully qualified path"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for `revm::primitives::Bytes` written as a fully qualified"
            "path instead of being imported and used as `Bytes`."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Importing `revm::primitives::Bytes` keeps code concise"
            "and consistent with project conventions."
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
            "let vm_code = revm::bytecode::Bytecode::new_raw(\n"
            "    revm::primitives::Bytes::from_static(&[0x00]),\n"
            ");\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "import Bytes and use it without the revm::primitives:: prefix"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {
                        "all": [
                            {"kind": "scoped_type_identifier"},
                            {"regex": "revm::primitives::Bytes"},
                        ]
                    },
                    {
                        "all": [
                            {"kind": "call_expression"},
                            {"regex": "revm::primitives::Bytes::"},
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
