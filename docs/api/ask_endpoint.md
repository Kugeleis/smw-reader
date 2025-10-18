# Ask Endpoint API

The `AskEndpoint` provides a powerful interface for querying a Semantic MediaWiki (SMW) instance. This document details how to use the `query` method and the `QueryBuilder` to construct and execute semantic queries.

## The `query` Method

The primary method for executing queries is `query`. It accepts either a raw SMW query string or a `QueryBuilder` instance.

### Basic Usage

You can pass a raw query string directly to the `query` method:

```python
from smw_reader import SMWClient

client = SMWClient(api_url="https://www.semantic-mediawiki.org/w/api.php")
ask_endpoint = client.ask

# Execute a simple query
results = ask_endpoint.query("[[Category:Help page]]")

print(results)
```

### With Additional Parameters

The `query` method also accepts additional parameters, such as `limit` and `sort`:

```python
# Limit the results to 5 and sort by name
results = ask_endpoint.query(
    "[[Category:Help page]]",
    limit=5,
    sort="Name"
)

print(results)
```

## The `QueryBuilder`

For more complex queries, the `QueryBuilder` provides a fluent, chainable interface for programmatic construction.

### Building a Simple Query

Here's how to build a simple query with a single condition:

```python
from smw_reader.endpoints.ask import QueryBuilder

query = QueryBuilder().add_conditions("Category:Help page")

results = ask_endpoint.query(query)

print(results)
```

### Chaining Methods

You can chain methods to add multiple conditions and printouts:

```python
query = (
    QueryBuilder()
    .add_conditions("Category:Help page", "Modification date::+
")
    .add_printouts("Name", "Modification date")
)

results = ask_endpoint.query(query)

print(results)
```
