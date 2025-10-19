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
# Recommended: Install with uv (fast, modern Python package manager)
uv pip install smw-reader

# Or with optional HTTP client support
uv pip install 'smw-reader[aiohttp]'  # For async HTTP with aiohttp
uv pip install 'smw-reader[httpx]'    # For async HTTP with httpx
uv pip install 'smw-reader[async]'    # For full async support

# Alternatively, use pip directly
pip install smw-reader
pip install 'smw-reader[aiohttp]'
pip install 'smw-reader[httpx]'
pip install 'smw-reader[async]'

# Development installation
git clone <repository-url>
cd smw-reader
uv sync
  
# To add dependencies during development, use:
uv add <package>
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



## Development

See the project's development guide in the documentation (Development) for setup, workflow, and contributing information.

## License

This project follows the guidelines specified in `AGENTS.md`.
