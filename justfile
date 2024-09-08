# Show help message
help:
    just -l

# Install package with dependencies
install:
	poetry install --with dev,test,lint

# Run pre-commit
lint:
	@pre-commit run --all-files
