"""Lint: tracing items with `tracing::` prefix."""

from __future__ import annotations

from typing import TYPE_CHECKING

from checkrs.lints.lint import Lint, Violation, make_config

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


class TracingPrefix(Lint):
    """tracing items with `tracing::` prefix."""

    @property
    def name(self) -> str:
        """Return the lint name."""
        return "tracing_prefix"

    @property
    def description(self) -> str:
        """Return the lint description."""
        return "tracing:: with prefix"

    @property
    def what_it_does(self) -> str:
        """Return what the lint does."""
        return (
            "Checks for fully-qualified `tracing::` macro and attribute usage"
            " such as `tracing::info!`, `tracing::error!`, `tracing::warn!`,"
            " `tracing::debug!`, `tracing::trace!`, and `#[tracing::instrument]`"
            " and requires importing them at the top of the file."
        )

    @property
    def why_restrict(self) -> str:
        """Return why this pattern is restricted."""
        return (
            "Fully-qualified `tracing::` paths are verbose. Import the item and"
            " use it directly.\n"
            "\n"
            "Bad:\n"
            "```rust\n"
            'tracing::error!("failed: {err}");\n'
            'tracing::warn!("warn");\n'
            "#[tracing::instrument]\n"
            "fn foo() {}\n"
            "```\n"
            "\n"
            "Good:\n"
            "```rust\n"
            "use tracing::{debug, error, info, instrument, trace, warn};\n"
            "\n"
            'error!("failed: {err}");\n'
            'warn!("warn");\n'
            "#[instrument]\n"
            "fn foo() {}\n"
            "```\n"
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
            'tracing::error!("error");' + "\n"
            'tracing::info!("info");' + "\n"
            "#[tracing::instrument]\n"
            "fn foo() {}\n"
            "\n"
            "// Good\n"
            "use tracing::{error, info, instrument};\n"
            "\n"
            'error!("error");' + "\n"
            'info!("info");' + "\n"
            "#[instrument]\n"
            "fn foo() {}\n"
            "```"
        )

    @property
    def help(self) -> str:
        """Return help text."""
        return "import `tracing` items and use them without the `tracing::` prefix"

    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a file and return any violations."""
        patterns: list[tuple[dict, str]] = [
            ({"pattern": "tracing::info!($$$ARGS)"}, "tracing::info! with prefix"),
            ({"pattern": "tracing::error!($$$ARGS)"}, "tracing::error! with prefix"),
            ({"pattern": "tracing::warn!($$$ARGS)"}, "tracing::warn! with prefix"),
            ({"pattern": "tracing::debug!($$$ARGS)"}, "tracing::debug! with prefix"),
            ({"pattern": "tracing::trace!($$$ARGS)"}, "tracing::trace! with prefix"),
            (
                {"all": [{"kind": "attribute_item"}, {"regex": "tracing::instrument"}]},
                "tracing::instrument with prefix",
            ),
        ]
        violations: list[Violation] = []
        for rule, message in patterns:
            config = make_config(rule=rule)
            for m in node.find_all(config):
                r = m.range()
                violations.append(
                    Violation(
                        lint_name=self.name,
                        file_path=file_path,
                        line=r.start.line + 1,
                        column=r.start.column + 1,
                        message=message,
                    )
                )
        violations.sort(key=lambda v: (v.line, v.column))
        return violations
