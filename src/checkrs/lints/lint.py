"""Abstract base class for checkrs lints."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import ast_grep_py


@dataclass(frozen=True)
class Violation:
    """A single lint violation found in a file."""

    lint_name: str
    file_path: Path
    line: int
    column: int
    message: str


@lru_cache(maxsize=256)
def _cached_config(key: str) -> ast_grep_py.Config:
    return json.loads(key)


def make_config(**kwargs: object) -> ast_grep_py.Config:
    """Create an ast-grep config from keyword arguments."""
    return _cached_config(json.dumps(kwargs, sort_keys=True))


class Lint(ABC):
    """Abstract base class for a checkrs lint."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the clippy-style lint name, e.g. ``absolute_paths``."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a one-line summary of what the lint checks."""

    @property
    @abstractmethod
    def what_it_does(self) -> str:
        """Return a detailed explanation of what the lint does."""

    @property
    @abstractmethod
    def why_restrict(self) -> str:
        """Return an explanation of why this pattern should be restricted."""

    @property
    @abstractmethod
    def known_issues(self) -> str:
        """Return known limitations or edge cases."""

    @property
    @abstractmethod
    def example(self) -> str:
        """Return example code showing the violation and/or fix."""

    @property
    @abstractmethod
    def help(self) -> str:
        """Return a short help message explaining the rule or fix."""

    @abstractmethod
    def check(self, file_path: Path, node: ast_grep_py.SgNode) -> list[Violation]:
        """Check a single file and return any violations."""
