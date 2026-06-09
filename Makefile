# Default target
.DEFAULT_GOAL := help

.PHONY: lock install lint lint-fix test types help

# Create a lockfile
lock:
	uv lock

# Install dependencies from lockfile
install:
	uv sync --frozen

# Run development services in the background
up:
	- docker-compose up -d
	- @echo "Mailpit is now available: http://localhost:8025"

# Check for linting issues
lint:
	uv run ruff check

# Fix linting issues
lint-fix:
	uv run ruff format

# Run all tests
test:
	uv run pytest

# Check types
types:
	uv run ty check

# Show help
help:
	@echo "Makefile commands:"
	@echo "  make lock       - Create a lockfile (uv lock)"
	@echo "  make install    - Install dependencies (uv sync --frozen)" 
	@echo "  make up    	 - Run development services in the background (docker-compose up -d)"
	@echo "  make lint       - Check for linting issues (uv run ruff check)"
	@echo "  make lint-fix   - Fix linting issues (uv run ruff format)"
	@echo "  make test       - Run all tests (uv run pytest)"
	@echo "  make types      - Check types (uv run ty check)"
