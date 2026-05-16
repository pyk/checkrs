.PHONY: check
check: ## Run code quality tools.
	@echo "Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "Linting code"
	@uv run ruff check --ignore-noqa
	@echo "Running type checker"
	@uv run pyrefly check --no-progress-bar --min-severity warn

.PHONY: bin
bin: ## Install local binary
	@echo "Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "Installing local binary"
	@uv tool install . --editable

.PHONY: test
test: ## Run tests. Optionally pass a test file as argument (e.g., make test ./path/to/file.py).
	@echo "Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "Running tests"
	@uv run pytest $(filter-out $@,$(MAKECMDGOALS))

# Catch-all target to handle extra arguments passed to make
%:
	@
