# Show help message
help:
    just -l

# Install package with dependencies
install:
	poetry install --with dev

# Run pre-commit
lint:
	@pre-commit run --all-files
