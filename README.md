# SMW Reader

A modular Python client library for accessing Semantic MediaWiki (SMW) API endpoints.

## Features

- **🚀 Auto-Formatted Printouts**: No more manual "?" prefixes - just pass plain property names!
- **🎯 Convenience Methods**: Purpose-built methods for common query patterns (`query_category`, `query_property_value`, etc.)
- **🔄 Full Backward Compatibility**: All existing code works unchanged
- **🏗️ Modular Design**: Following the open/closed principle, easily extensible with new API endpoints
- **🛡️ Type Safety**: Full type hints throughout the codebase
- **🚨 Robust Error Handling**: Custom exceptions for different error scenarios
- **📦 No External Dependencies**: Uses only Python standard library for HTTP requests
- **🧪 Comprehensive Testing**: Full test suite with pytest (59 tests)

## Installation

```bash
# Install from PyPI (when published)
pip install smw-reader

# Or with optional HTTP client support
pip install smw-reader[aiohttp]  # For async HTTP with aiohttp
pip install smw-reader[httpx]    # For async HTTP with httpx
pip install smw-reader[async]    # For full async support

# Development installation
git clone <repository-url>
cd smw-reader
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

# Simple property query with auto-formatted printouts
result = ask_endpoint.query_property_value(
    property_name="Category",
    value="Person",
    printouts=["Name", "Age"]  # Auto-formatted to ["?Name", "?Age"]
)

# Category query with auto-formatted printouts
result = ask_endpoint.query_category(
    category="Person",
    printouts=["Name", "Age", "Email"],  # No need for "?" prefix!
    limit=10
)
print(result)
```

## Available Endpoints

### Ask Endpoint

The `ask` endpoint allows you to execute semantic queries using SMW's query language with enhanced convenience methods.

#### Enhanced Convenience Methods (Recommended)

```python
# Query by property value - printouts auto-formatted
result = ask_endpoint.query_property_value(
    property_name="License",
    value="GPL",
    printouts=["Name", "Homepage URL", "Description"]  # Auto-formatted!
)

# Query by category - printouts auto-formatted
result = ask_endpoint.query_category(
    category="Software",
    printouts=["Name", "License", "Version"],  # Auto-formatted!
    limit=20
)

# Query by concept - printouts auto-formatted
result = ask_endpoint.query_concept(
    concept="Important People",
    printouts=["Name", "Birth date", "Occupation"]  # Auto-formatted!
)
```

#### Traditional Methods (Required for Advanced Cases)

```python
# Direct query execution - needed for complex SMW syntax
result = ask_endpoint.execute(query="[[Category:Person]]|?Name=Full Name|?Birth date=Born")

# Custom property labels and aliases
result = ask_endpoint.ask("[[Category:Software]]|?Name=Title|?License=License Type", limit=5)

# Subqueries and property chains
result = ask_endpoint.execute(
    query="[[Category:Person]]|?Works on.Name=Projects|?Lives in.Population=City Size"
)

# Complex conditions with OR operations
result = ask_endpoint.execute(
    query="[[Category:Software]] OR [[Category:Library]]|?Name|?License"
)

# Structured query with multiple conditions (enhanced with auto-formatting)
result = ask_endpoint.query_pages(
    conditions=AskEndpoint.build_conditions(["Category:Person", "Age::>25"]),
    printouts=["Name", "Age"],  # Now auto-formatted!
    limit=10,
    sort="Name",
    order="asc"
)
```

#### Backward Compatibility

```python
# Old format still works (fully backward compatible)
result = ask_endpoint.query_category(
    category="Software",
    printouts=["?Name", "?License"]  # Pre-formatted printouts work too
)

# Mixed formats are supported
result = ask_endpoint.query_property_value(
    property_name="Type",
    value="Application",
    printouts=["Name", "?License", "Version"]  # Mix of formats works!
)
```

## Key Features & Enhancements

### 🚀 Auto-Formatted Printouts

One of the major enhancements is **automatic printout formatting**. You no longer need to manually add "?" prefixes to property names:

```python
# ✅ NEW: Simple and clean
result = ask_endpoint.query_category(
    category="Software",
    printouts=["Name", "License", "Homepage URL"]  # Auto-formatted!
)

# ⚠️ OLD: Required manual formatting
result = ask_endpoint.query_category(
    category="Software",
    printouts=["?Name", "?License", "?Homepage URL"]  # Manual "?" prefix
)
```

### 🎯 Convenience Methods

Choose the right method for your use case:

| Method | Use Case | Auto-Formatting | Advanced SMW Features |
|--------|----------|-----------------|----------------------|
| `query_property_value()` | Simple property-value queries | ✅ Yes | ❌ Limited |
| `query_category()` | Basic category queries | ✅ Yes | ❌ Limited |
| `query_concept()` | Basic concept queries | ✅ Yes | ❌ Limited |
| `query_pages()` | Multi-condition queries with sorting | ✅ Yes (printouts) | ⚠️ Partial |
| `ask()` / `execute()` | Advanced SMW syntax & complex queries | ❌ No | ✅ Full Support |

**When to use Enhanced Methods (80% of cases):**
- Simple category/property queries
- Standard printouts without aliases
- Basic filtering and sorting

**When to use Traditional Methods (20% of cases):**
- Custom property labels (`?Name=Title`)
- Subqueries with dot notation (`?Works on.Name`)
- OR operations (`[[A]] OR [[B]]`)
- Parser functions and templates
- Advanced output formatting

### 🔄 Full Backward Compatibility

All existing code continues to work unchanged:
- Pre-formatted printouts (with "?") still work
- Helper methods `build_conditions()` and `build_printouts()` remain available
- All parameter names and method signatures are preserved
- Mixed formats are supported in the same call

### 🚧 When Enhanced Methods Have Limitations

The enhanced convenience methods are designed for **common, straightforward queries** (80% of use cases). For advanced SMW features, use traditional methods:

**❌ Enhanced methods cannot handle:**
```python
# Custom property aliases
"[[Category:Software]]|?Name=Software Title|?License=License Type"

# Property chains/subqueries
"[[Category:Person]]|?Works on.Name=Projects|?Lives in.Population=City Size"

# OR operations
"[[Category:Software]] OR [[Category:Library]]|?Name"

# Parser functions
"[[Category:Person]]|?{{#if:{{CURRENTUSER}}|Birth date|Born}}=Date"

# Mathematical/aggregation functions
"[[Category:City]]|?#ask:{{#ask:[[Located in::{{FULLPAGENAME}}]]|format=count}}=Districts"
```

**✅ For these cases, use traditional methods:**
```python
# Full SMW syntax support
result = ask_endpoint.execute(query="[[Category:Software]]|?Name=Title|?License=Type")
result = ask_endpoint.ask("[[A]] OR [[B]]|?Name", limit=10)
```

## Architecture

The library follows a modular architecture:

- **`SMWClient`**: Main client class that handles HTTP requests and endpoint registration
- **`APIEndpoint`**: Abstract base class for API endpoints (open/closed principle)
- **`HTTPClient`**: Abstract interface for HTTP clients (dependency injection)
- **`RequestsHTTPClient`**: Concrete implementation using urllib

## Real-World Examples

### Free Software Foundation Directory

```python
from smw_reader import SMWClient
from smw_reader.endpoints.ask import AskEndpoint

# Connect to FSF Directory
client = SMWClient("https://directory.fsf.org/w/")
ask_endpoint = AskEndpoint(client)

# Find all GNU software with license info
gnu_software = ask_endpoint.query_property_value(
    property_name="Is GNU",
    value="Yes",
    printouts=["Name", "License", "Interface", "Homepage URL"],
    limit=20
)

# Find featured software
featured = ask_endpoint.query_property_value(
    property_name="Featured date",
    value="+",  # SMW syntax for "any value"
    printouts=["Name", "License", "Homepage URL", "Full description"]
)
```

### MediaWiki with Categories

```python
# Query pages in a category
articles = ask_endpoint.query_category(
    category="Computer Science",
    printouts=["Author", "Publication date", "Abstract"],
    limit=50
)

# Query with multiple conditions using query_pages
complex_query = ask_endpoint.query_pages(
    conditions=AskEndpoint.build_conditions([
        "Category:Research",
        "Publication year::>2020"
    ]),
    printouts=["Title", "Authors", "DOI", "Abstract"],  # Auto-formatted!
    limit=25,
    sort="Publication date",
    order="desc"
)
```

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

## Migration Guide

### Upgrading to Enhanced Version

**Good news**: No breaking changes! Your existing code will continue to work exactly as before.

**Even better news**: You can now simplify ~80% of your queries by removing manual formatting:

### Assessment: Should You Migrate?

**✅ Migrate to Enhanced Methods if your queries use:**
- Simple category queries: `[[Category:X]]`
- Basic property filters: `[[Property::Value]]`
- Standard printouts: `?Name|?License|?Version`
- Basic sorting and limits

**⚠️ Keep Traditional Methods if your queries use:**
- Custom labels: `?Name=Title|?License=Type`
- Property chains: `?Works on.Name|?Lives in.Population`
- OR operations: `[[A]] OR [[B]]`
- Parser functions or complex SMW syntax

#### Before (Still Works)
```python
# Old way - manual formatting required
printouts = AskEndpoint.build_printouts(["Name", "License", "Version"])
result = ask_endpoint.query_category("Software", printouts=printouts)

# Or with manual "?" prefixes
result = ask_endpoint.query_category(
    "Software",
    printouts=["?Name", "?License", "?Version"]
)
```

#### After (Recommended)
```python
# New way - auto-formatted, cleaner
result = ask_endpoint.query_category(
    "Software",
    printouts=["Name", "License", "Version"]  # No "?" needed!
)
```

#### Mixed Migration (Supported)
```python
# You can even mix formats during migration
result = ask_endpoint.query_category(
    "Software",
    printouts=["Name", "?License", "Version"]  # Mixed formats work!
)
```

### Helper Functions Still Available

The `build_conditions()` and `build_printouts()` helper functions remain available for advanced use cases or if you prefer explicit formatting:

```python
# Still available if you prefer explicit control
conditions = AskEndpoint.build_conditions(["Category:Software", "License::GPL"])
printouts = AskEndpoint.build_printouts(["Name", "Version"])  # Optional now!

result = ask_endpoint.query_pages(
    conditions=conditions,
    printouts=printouts  # Or just pass ["Name", "Version"] directly
)
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
