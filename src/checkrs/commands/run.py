"""Implementation of the ``run`` command."""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from checkrs.lints import get_all_lints

if TYPE_CHECKING:
    from pathlib import Path

    from checkrs.lints.lint import Violation


def _collect_files(path: Path) -> tuple[list[Path], str | None]:
    if path.is_file():
        if path.suffix != ".rs":
            return [], "not a Rust file"
        return [path], None
    if path.is_dir():
        return list(path.rglob("*.rs")), None
    return [], "path does not exist"


def _check_file(file_path: Path) -> list[Violation]:
    violations: list[Violation] = []
    try:
        source = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"warning: could not read {file_path}: {exc}\n")
        return violations

    for lint in get_all_lints():
        violations.extend(lint.check(file_path, source))

    return violations


def run(path: Path) -> int:
    """Run all lints against the given path and return an exit code."""
    files, error = _collect_files(path)
    if error is not None:
        sys.stderr.write(f"error: {error}: {path}\n")
        return 1

    all_violations: list[Violation] = []
    max_workers = min(32, (os.cpu_count() or 1) + 4)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(_check_file, files)

    for violation_list in results:
        all_violations.extend(violation_list)

    if not all_violations:
        return 0

    lint_map = {lint.name: lint for lint in get_all_lints()}
    grouped: dict[str, list[Violation]] = defaultdict(list)
    for v in all_violations:
        grouped[v.lint_name].append(v)

    for lint_name, violations in grouped.items():
        lint = lint_map[lint_name]
        sys.stdout.write(f"error[{lint_name}]: {lint.description}\n")
        for v in violations:
            sys.stdout.write(f"  --> {v.file_path}:{v.line}:{v.column}\n")
            sys.stdout.write(f"      {v.message}\n")
        sys.stdout.write("\n")

    return 1
