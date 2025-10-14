# SMW Reader

A modular Python client library for accessing Semantic MediaWiki (SMW) API endpoints.

## Features

- **Modular Design**: Following the open/closed principle, easily extensible with new API endpoints
- **Type Safety**: Full type hints throughout the codebase
- **Robust Error Handling**: Custom exceptions for different error scenarios
- **No External Dependencies**: Uses only Python standard library for HTTP requests
- **Comprehensive Testing**: Full test suite with pytest

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd smw-reader

# Install dependencies
uv sync
```

## Quick Start

```python
from smw_reader import SMWClient
from smw_reader.endpoints.ask import AskEndpoint

# Create a client instance
client = SMWClient("https://your-wiki.org/w/")

# Register the ask endpoint
ask_endpoint = AskEndpoint(client)
client.register_endpoint(ask_endpoint)

# Get the ask endpoint
ask = client.get_endpoint("ask")

# Execute a semantic query
result = ask.ask("[[Category:Person]]|?Name|?Age", limit=10)
print(result)
```

## Available Endpoints

### Ask Endpoint

The `ask` endpoint allows you to execute semantic queries using SMW's query language.

```python
# Simple query
result = ask.execute(query="[[Category:Person]]")

# Query with parameters
result = ask.ask(
    "[[Category:Person]]|?Name|?Age",
    limit=5,
    sort="Name",
    order="asc"
)

# Structured query
result = ask.query_pages(
    conditions=["[[Category:Person]]", "[[Age::>25]]"],
    printouts=["?Name", "?Age"],
    limit=10
)
```

## Architecture

The library follows a modular architecture:

- **`SMWClient`**: Main client class that handles HTTP requests and endpoint registration
- **`APIEndpoint`**: Abstract base class for API endpoints (open/closed principle)
- **`HTTPClient`**: Abstract interface for HTTP clients (dependency injection)
- **`RequestsHTTPClient`**: Concrete implementation using urllib

## Error Handling

The library provides specific exceptions for different error scenarios:

```python
from smw_reader.exceptions import (
    SMWAPIError,           # Base API error
    SMWConnectionError,    # Network/connection issues
    SMWServerError,        # Server-side errors
    SMWValidationError,    # Invalid parameters
    SMWAuthenticationError # Authentication failures
)

try:
    result = ask.ask("[[Category:Test]]")
except SMWConnectionError:
    print("Network issue")
except SMWAPIError as e:
    print(f"API error: {e}")
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=smw_reader
```

### Adding New Endpoints

To add a new API endpoint, inherit from `APIEndpoint`:

```python
from smw_reader.interfaces import APIEndpoint
from typing import Any, Dict

class NewEndpoint(APIEndpoint):
    @property
    def endpoint_name(self) -> str:
        return "new_endpoint"

    def execute(self, **params: Any) -> Dict[str, Any]:
        # Implementation here
        return self._client.make_request("new_action", params)

# Register with client
client.register_endpoint(NewEndpoint(client))
```

## Development

This project uses modern Python development tools for code quality and development workflows.

### Quick Start

Initialize the development environment:
```bash
# Using Task (recommended)
task init

# Or using uv and duty directly
uv sync --all-extras
python -m duty init_project
```

### Available Tasks

#### Using Task (Taskfile.yaml)

```bash
# Development setup
task install          # Install dependencies
task install-dev      # Install development dependencies
task init            # Initialize project for development

# Code quality
task format          # Format code with ruff
task lint            # Run linting with ruff
task lint-fix        # Run linting and fix issues
task type-check      # Run type checking with mypy

# Testing
task test            # Run tests with pytest
task test-cov        # Run tests with coverage
task test-watch      # Run tests in watch mode

# Security and dependencies
task security        # Run security checks with bandit
task deps-check      # Check dependencies for vulnerabilities

# Build and maintenance
task build           # Build the package
task clean           # Clean up build artifacts
task update          # Update dependencies

# Workflows
task check           # Run all checks (format, lint, type-check, test)
task ci              # Run CI checks
task dev-setup       # Complete development environment setup
task release-check   # Run all checks before release
```

#### Using Duty directly

```bash
python -m duty format      # Format code
python -m duty lint        # Lint code
python -m duty test        # Run tests
python -m duty check_all   # Run all checks
```

### Development Tools

- **[uv](https://github.com/astral-sh/uv)**: Fast Python package manager
- **[ruff](https://github.com/astral-sh/ruff)**: Fast Python linter and formatter
- **[mypy](https://mypy-lang.org/)**: Static type checker
- **[pytest](https://pytest.org/)**: Testing framework
- **[duty](https://github.com/pawamoy/duty)**: Task runner for development
- **[Task](https://taskfile.dev/)**: Task runner (optional convenience wrapper)
- **[pre-commit](https://pre-commit.com/)**: Git hooks for code quality

### Pre-commit Hooks

Install pre-commit hooks to automatically run quality checks:
```bash
task pre-commit-install
# Or: pre-commit install
```

## License

This project follows the guidelines specified in `AGENTS.md`.

## Contributing

Please follow the coding standards and architectural principles outlined in `AGENTS.md` when contributing to this project.

### Development Workflow

1. Set up development environment: `task dev-setup`
2. Make your changes
3. Run quality checks: `task check`
4. Run tests: `task test`
5. Commit your changes (pre-commit hooks will run automatically)
6. Submit a pull request
