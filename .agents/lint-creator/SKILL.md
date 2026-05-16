---
name: lint-creator
description:
    Guide for creating new checkrs lints from start to finish. Use when the
    user asks to add, create, or implement a new lint rule for the checkrs
    Rust linter. Covers lint naming, class implementation, registration,
    and test writing.
metadata:
    short-description: Create a new checkrs lint
---

# Lint Creator

Create a new checkrs lint rule that checks Rust source files for a specific
pattern and reports violations.

## Naming Convention

Use clippy-style lint names:

- Lowercase snake_case
- Descriptive and direct (e.g. `absolute_paths`, `byte_char_slices`)
- Prefer noun phrases or verb-noun pairs that describe the problem

Examples:

- `mod_rs_missing_docs`
- `absolute_paths`
- `absurd_extreme_comparisons`
- `alloc_instead_of_core`
- `as_ptr_cast_mut`
- `assign_op_pattern`
- `byte_char_slices`
- `disallowed_macros`

## File Structure

Create or edit these files in order:

1. `src/checkrs/lints/<lint_name>.py` — lint implementation
2. `src/checkrs/lints/__init__.py` — registration
3. `tests/lints/test_<lint_name>.py` — tests

## Step 1: Create the Lint File

Create `src/checkrs/lints/<lint_name>.py` using the template in
[assets/lint-template.py](assets/lint-template.py) as a starting point.

### Implementation Rules

- Import `ast_grep_py` for AST-based matching on Rust source code
- Import `Lint` and `Violation` from `checkrs.lints.lint`
- Use `from __future__ import annotations` and `TYPE_CHECKING` for `pathlib.Path`
- The `check` method receives `(file_path: Path, source: str)` and returns
  `list[Violation]`
- Return an empty list when the file is clean
- Use `ast_grep_py.SgRoot(source, "rust")` to parse the file
- Use `ast_grep_py.Config(rule={...})` for matching rules
- Set `line` and `column` from the matched node's `range()` when possible
- If no precise match exists, default to `line=1, column=1`
- The `message` in `Violation` should be a short tag (e.g. ``"missing"``,
  ``"deprecated"``) — not a full sentence. The full explanation lives in
  `description` and `help`
- The `description` must be short and read naturally with a count prefix:
  ``"3 {description}"``. Example: ``"mod.rs files missing \`!\`\` module doc"``
- All metadata properties (`what_it_does`, `why_restrict`, `known_issues`,
  `example`, `help`) must be filled in
- `help` should state the rule or fix in one short sentence. It prints once
  per lint, after all file locations

## Step 2: Register the Lint

Open `src/checkrs/lints/__init__.py` and append the new lint class to the
`get_all_lints()` return list:

```python
from checkrs.lints.<lint_name> import <ClassName>

def get_all_lints() -> list[Lint]:
    return [
        ModRsMissingDocs(),
        <ClassName>(),
    ]
```

Keep imports inside `TYPE_CHECKING` when possible, matching the existing style.

## Step 3: Write Tests

Create `tests/lints/test_<lint_name>.py` using the template in
[assets/test-template.py](assets/test-template.py).

### Test Guidelines

- Use `CliRunner` from `typer.testing` and invoke `checkrs.main:app`
- Provide at minimum two tests: one that triggers the lint and one that does
  not
- Use `tmp_path` from pytest to create temporary Rust files
- Verify the exit code and output contain:
  - The lint name in the header: ``error[{lint_name}]:``
  - The count and description: ``"1 {description}"``
  - The file location: ``"--> {file}:{line}:{column}"``
  - The help line: ``"help: {lint.help}"``
- Keep test functions focused on a single behavior each
- Follow the existing test file style for imports and docstrings

### Output Format

The runner prints one block per lint:

```
error[lint_name]: 3 lint description here
  --> path/to/file.rs:1:1
  --> path/to/other.rs:4:2
help: short rule or fix text
```

## Validation

After implementation, run the following to verify correctness:

```bash
make check   # ruff + pyrefly
make test    # pytest
```

Fix any errors before finishing.
