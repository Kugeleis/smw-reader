# SMW Reader

A modular Python client library for accessing Semantic MediaWiki (SMW) API endpoints.

## Features

- **🚀 Fluent Query Builder**: A programmatic and readable way to construct complex queries.
- **🎯 Convenience Methods**: A purpose-built method for querying categories (`query_category`).
- **🏗️ Modular Design**: Following the open/closed principle, easily extensible with new API endpoints.
- **🛡️ Type Safety**: Full type hints throughout the codebase.
- **🚨 Robust Error Handling**: Custom exceptions for different error scenarios.
- **📦 No External Dependencies**: Uses only Python standard library for HTTP requests.
- **🧪 Comprehensive Testing**: Full test suite with pytest.

## Installation

```bash
# Recommended: Install with uv (fast, modern Python package manager)
uv pip install smw-reader

# Or with optional HTTP client support
uv pip install 'smw-reader[aiohttp]'  # For async HTTP with aiohttp
uv pip install 'smw-reader[httpx]'    # For async HTTP with httpx
uv pip install 'smw-reader[async]'    # For full async support

# Alternatively, use pip directly
pip install smw-reader

# Development installation
git clone <repository-url>
cd smw-reader
uv sync
```

## Quick Start

```python
from smw_reader import SMWClient, QueryBuilder

# Create a client instance
site = SMWClient("https://your-wiki.org/w/")

# Build a query using the QueryBuilder
builder = QueryBuilder()
builder.add_conditions("Category:Person").add_printouts("Name", "Age")

# Execute the query
result = site.ask.query(builder, limit=10)

print(result)

# You can also use the convenience method for categories
result_category = site.ask.query_category("Person", printouts=["Name", "Age"], limit=10)

print(result_category)
```

## Building Queries

The recommended way to build queries is using the `QueryBuilder`, which provides a fluent interface for adding conditions and printouts.

### `QueryBuilder`

The `QueryBuilder` allows you to construct complex SMW queries programmatically.

```python
from smw_reader import QueryBuilder

# Start with a new builder
builder = QueryBuilder()

# Chain methods to add conditions and printouts
builder.add_conditions(
    "Category:Software",
    "License::GPL"
).add_printouts(
    "Name",
    "Homepage URL",
    "Version"
)

# The builder can be passed directly to the query method
result = site.ask.query(builder, limit=20)
```

### Advanced Queries with Dictionaries

For more complex conditions, you can pass a dictionary to `add_conditions`. This is particularly useful for queries involving operators (like `>`, `<`, `!`) or when you need to be explicit about the property you are querying.

The dictionary can have the following keys:

-   `key`: The property or category name (e.g., "Creation date", "Category").
-   `value`: The value to match.
-   `operator`: (Optional) A comparison operator, such as `>`, `<`, `>=`, `<=`, or `!`.

#### Example: Querying by Category and Date

Here is how to query for pages in the "Software" category that were created before May 5th, 2024:

```python
from smw_reader import QueryBuilder

builder = QueryBuilder()

builder.add_conditions(
    {"key": "Category", "value": "Software"},
    {"key": "Creation date", "operator": "<", "value": "2024-05-05"}
).add_printouts(
    "Name",
    "Version"
)

result = site.ask.query(builder)
```

### Raw Query Strings

For very complex queries or direct control, you can still use raw SMW query strings.

```python
# Subqueries, custom labels, and other advanced features
raw_query = "[[Category:Person]]|?Works on.Name=Projects|?Lives in.Population=City Size"
result = site.ask.query(raw_query)
```

### Convenience Methods

For common tasks, convenience methods provide a simpler interface.

#### `query_category()`

Query all pages in a specific category.

```python
# Query by category - printouts are auto-formatted
result = site.ask.query_category(
    category="Software",
    printouts=["Name", "License", "Version"],  # No "?" prefix needed!
    limit=20
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
    result = site.ask.query("[[Category:Test]]")
except SMWConnectionError:
    print("Network issue")
except SMWAPIError as e:
    print(f"API error: {e}")
```

## Architecture

The library follows a modular architecture:

- **`SMWClient`**: Main client class that handles HTTP requests and endpoint registration.
- **`APIEndpoint`**: Abstract base class for API endpoints.
- **`QueryBuilder`**: A fluent interface for building query strings.
- **`HTTPClient`**: Abstract interface for HTTP clients.
- **`RequestsHTTPClient`**: Concrete implementation using urllib.

## Development

See the project's development guide in the documentation (`docs/sphinx/DEVELOPMENT.md`) for setup, workflow, and contributing information.
