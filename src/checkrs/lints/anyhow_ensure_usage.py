"""Lint: manual if/bail! instead of ensure!."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class AnyhowEnsureUsage(Lint):
    """manual if/bail! instead of ensure!."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "anyhow_ensure_usage"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "manual if/bail! instead of ensure!"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Using `ensure!` is more concise and readable than an if statement"
            "with a `bail!` or `return Err(anyhow::anyhow!())` in the body."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Instead of: ```rust if !index_html_path.exists() { bail!("
            "\"index.html not found in cargo doc output directory '{}'\","
            "cargo_doc_output_dir.display() ); } ```"
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
            "if !index_html_path.exists() {\n"
            "    bail!(\n"
            "        \"index.html not found in cargo doc output directory '{}'\",\n"
            "        cargo_doc_output_dir.display()\n"
            "    );\n"
            "}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "use ensure! instead of manual if/bail!"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        config = make_config(
            rule={
                "any": [
                    {
                        "all": [
                            {"pattern": "if !$COND { bail!($$$ARGS); }"},
                            {"not": {"pattern": "if !($$$INNER) { bail!($$$ARGS); }"}},
                        ]
                    },
                    {
                        "all": [
                            {
                                "pattern": "if !$COND { return "
                                "Err(anyhow::anyhow!($$$ARGS)); }"
                            },
                            {
                                "not": {
                                    "pattern": "if !($$$INNER) { return "
                                    "Err(anyhow::anyhow!($$$ARGS)); }"
                                }
                            },
                        ]
                    },
                    {
                        "all": [
                            {"pattern": "if $COND { bail!($$$ARGS); }"},
                            {
                                "has": {
                                    "any": [
                                        {"pattern": "$$$OBJ.is_empty()"},
                                        {"pattern": "$$$OBJ.is_none()"},
                                        {"pattern": "$$$OBJ.is_err()"},
                                    ]
                                }
                            },
                        ]
                    },
                    {
                        "all": [
                            {
                                "pattern": "if $COND { return "
                                "Err(anyhow::anyhow!($$$ARGS)); }"
                            },
                            {
                                "has": {
                                    "any": [
                                        {"pattern": "$$$OBJ.is_empty()"},
                                        {"pattern": "$$$OBJ.is_none()"},
                                        {"pattern": "$$$OBJ.is_err()"},
                                    ]
                                }
                            },
                        ]
                    },
                    {"pattern": "if $LEFT >= $RIGHT { bail!($$$ARGS); }"},
                    {"pattern": "if $LEFT > $RIGHT { bail!($$$ARGS); }"},
                    {"pattern": "if $LEFT == $RIGHT { bail!($$$ARGS); }"},
                    {"pattern": "if $LEFT != $RIGHT { bail!($$$ARGS); }"},
                    {"pattern": "if $LEFT <= $RIGHT { bail!($$$ARGS); }"},
                    {"pattern": "if $LEFT < $RIGHT { bail!($$$ARGS); }"},
                    {
                        "pattern": "if $LEFT >= $RIGHT { return "
                        "Err(anyhow::anyhow!($$$ARGS)); }"
                    },
                    {
                        "pattern": "if $LEFT > $RIGHT { return "
                        "Err(anyhow::anyhow!($$$ARGS)); }"
                    },
                    {
                        "pattern": "if $LEFT == $RIGHT { return "
                        "Err(anyhow::anyhow!($$$ARGS)); }"
                    },
                    {
                        "pattern": "if $LEFT != $RIGHT { return "
                        "Err(anyhow::anyhow!($$$ARGS)); }"
                    },
                    {
                        "pattern": "if $LEFT <= $RIGHT { return "
                        "Err(anyhow::anyhow!($$$ARGS)); }"
                    },
                    {
                        "pattern": "if $LEFT < $RIGHT { return "
                        "Err(anyhow::anyhow!($$$ARGS)); }"
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
