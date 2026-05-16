"""Implementation of the ``run`` command."""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from checkrs.lints import get_all_lints

if TYPE_CHECKING:
    from pathlib import Path

    from checkrs.lints.lint import Lint, Violation

_SUPPRESSION_RE = re.compile(
    r"//\s*checkrs:\s*(?P<action>allow|ignore)\s*(?:\((?P<names>[^)]+)\))?"
)


def _collect_files(path: Path) -> tuple[list[Path], str | None]:
    if path.is_file():
        if path.suffix != ".rs":
            return [], "not a Rust file"
        return [path], None
    if path.is_dir():
        return list(path.rglob("*.rs")), None
    return [], "path does not exist"


def _parse_suppressions(source: str) -> set[tuple[int, str | None]]:
    """Return a set of (line, lint_name | None) suppressions.

    A ``None`` lint_name means the suppression applies to all lints.
    Suppressions affect both the comment line and the following line.
    """
    suppressions: set[tuple[int, str | None]] = set()
    for line_no, line in enumerate(source.splitlines(), start=1):
        match = _SUPPRESSION_RE.search(line)
        if match is None:
            continue
        action = match.group("action")
        names_str = match.group("names")
        if action == "ignore":
            # applies to all lints on this line and the next line
            suppressions.add((line_no, None))
            suppressions.add((line_no + 1, None))
        elif action == "allow" and names_str is not None:
            for raw_name in names_str.split(","):
                stripped = raw_name.strip()
                if stripped:
                    suppressions.add((line_no, stripped))
                    suppressions.add((line_no + 1, stripped))
    return suppressions


def _check_file(
    file_path: Path,
) -> tuple[list[Violation], list[Violation]]:
    active: list[Violation] = []
    suppressed: list[Violation] = []
    try:
        source = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"warning: could not read {file_path}: {exc}\n")
        return active, suppressed

    suppressions = _parse_suppressions(source)

    for lint in get_all_lints():
        for violation in lint.check(file_path, source):
            if (violation.line, violation.lint_name) in suppressions:
                suppressed.append(violation)
                continue
            if (violation.line, None) in suppressions:
                suppressed.append(violation)
                continue
            active.append(violation)

    return active, suppressed


def _print_results(
    violations: dict[str, list[Violation]],
    suppressed: dict[str, list[Violation]],
    lint_map: dict[str, Lint],
) -> None:
    all_lint_names = set(violations.keys()) | set(suppressed.keys())
    for lint_name in sorted(all_lint_names):
        lint = lint_map[lint_name]
        vlist = violations.get(lint_name, [])
        slist = suppressed.get(lint_name, [])
        count = len(vlist)
        ignored = len(slist)
        if vlist:
            header = f"error[{lint_name}]: {count} {lint.description}"
            if ignored:
                header += f" ({ignored} ignored)"
            sys.stdout.write(f"{header}\n")
            for v in vlist:
                sys.stdout.write(f"  --> {v.file_path}:{v.line}:{v.column}\n")
            sys.stdout.write(f"help: {lint.help}\n")
            sys.stdout.write("\n")
        elif ignored:
            sys.stdout.write(
                f"note[{lint_name}]: {ignored} {lint.description} ignored\n",
            )
            for v in slist:
                sys.stdout.write(f"  --> {v.file_path}:{v.line}:{v.column}\n")
            sys.stdout.write("\n")


def run(paths: list[Path]) -> int:
    """Run all lints against the given paths and return an exit code."""
    files: list[Path] = []
    errors: list[str] = []

    for path in paths:
        collected, error = _collect_files(path)
        if error is not None:
            errors.append(f"error: {error}: {path}")
        else:
            files.extend(collected)

    if errors:
        for msg in errors:
            sys.stderr.write(msg + "\n")
        return 1

    all_violations: list[Violation] = []
    all_suppressed: list[Violation] = []
    max_workers = min(32, (os.cpu_count() or 1) + 4)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(_check_file, files)

    for active_list, suppressed_list in results:
        all_violations.extend(active_list)
        all_suppressed.extend(suppressed_list)

    if not all_violations and not all_suppressed:
        return 0

    lint_map = {lint.name: lint for lint in get_all_lints()}
    grouped: dict[str, list[Violation]] = defaultdict(list)
    for v in all_violations:
        grouped[v.lint_name].append(v)

    suppressed_grouped: dict[str, list[Violation]] = defaultdict(list)
    for v in all_suppressed:
        suppressed_grouped[v.lint_name].append(v)

    _print_results(grouped, suppressed_grouped, lint_map)
    return 1 if all_violations else 0
