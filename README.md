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

## License

This project follows the guidelines specified in `AGENTS.md`.

## Contributing

Please follow the coding standards and architectural principles outlined in `AGENTS.md` when contributing to this project.