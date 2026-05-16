"""Abstract base class for checkrs lints."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class Violation:
    """A single lint violation found in a file."""

    lint_name: str
    file_path: Path
    line: int
    column: int
    message: str


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

    @abstractmethod
    def check(self, file_path: Path, source: str) -> list[Violation]:
        """Check a single file and return any violations."""
