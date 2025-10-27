.PHONY: test test-verbose test-coverage test-html clean install

# Install dependencies
install:
	uv sync

# Run all tests
test:
	uv run pytest tests/ -vv

# Run tests with verbose output
test-verbose:
	uv run pytest tests/ -v

# Run tests with coverage
test-coverage:
	uv run pytest tests/ --cov=ram_python --cov-report=term-missing

# Run tests with HTML coverage report
test-html:
	uv run pytest tests/ --cov=ram_python --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Run specific test file
test-file:
	uv run pytest tests/test_api.py -v

# Run tests matching a pattern
test-pattern:
	uv run pytest tests/ -k $(PATTERN) -v

# Clean generated files
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Run main script
run:
	uv run python ram_python/main.py
