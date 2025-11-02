# SMW Reader Usage Examples

This document provides examples of how to use the `smw-reader` library to interact with a Semantic MediaWiki API. These examples cover the main endpoints and the `QueryBuilder` for constructing complex queries.

## `AskEndpoint`

The `AskEndpoint` is used to execute semantic queries using SMW's query language.

### Basic Query with a Raw String

You can execute a query by passing a raw SMW query string to the `query` method:

```python
from smw_reader import SMWClient

# Initialize the client with the API endpoint URL
site = SMWClient("https://www.semantic-mediawiki.org/w/api.php")

# Define a query to find all cities and retrieve their population
query_string = "[[Category:Cities]]|?Population"

# Execute the query
results = site.ask.query(query_string)

# Print the results
print(results)
```

### Using the `QueryBuilder`

For more complex queries, the `QueryBuilder` provides a fluent interface for constructing queries programmatically.

```python
from smw_reader import SMWClient, QueryBuilder

site = SMWClient("https://www.semantic-mediawiki.org/w/api.php")

# Create a QueryBuilder instance
builder = QueryBuilder()

# Add conditions and printouts
builder.add_conditions("Category:Cities").add_printouts("Population")

# Execute the query using the builder
results = site.ask.query(builder)

print(results)
```

### `query_category` Convenience Method

The `query_category` method simplifies querying for pages within a specific category.

```python
from smw_reader import SMWClient

site = SMWClient("https://www.semantic-mediawiki.org/w/api.php")

# Query for pages in the 'Cities' category and get their population
results = site.ask.query_category("Cities", printouts=["Population"])

print(results)
```

### Using a Filter List

For better code organization, you can define your query conditions and printouts in a list and then unpack them into the `add_conditions` and `add_printouts` methods using the `*` operator. This is particularly useful when you have a dynamic set of filters.

```python
from smw_reader import SMWClient, QueryBuilder

site = SMWClient("https://www.semantic-mediawiki.org/w/api.php")

# Create a QueryBuilder instance
builder = QueryBuilder()

# Define conditions and printouts as lists
conditions = ["Category:Cities", "Population:>=1000000"]
printouts = ["Population", "Country"]

# Unpack the lists into the builder methods
builder.add_conditions(*conditions).add_printouts(*printouts)

# Execute the query
results = site.ask.query(builder)

print(results)
```

## `QueryBuilder`

The `QueryBuilder` is a powerful tool for building complex SMW queries in a structured way.

### Building a Complex Query

Here's an example of how to build a query with multiple conditions and printouts:

```python
from smw_reader import QueryBuilder

# Create a QueryBuilder instance
builder = QueryBuilder()

# Add multiple conditions
builder.add_conditions(
    "Category:Programming languages",
    {"key": "Has paradigm", "value": "Object-oriented"}
)

# Add multiple printouts
builder.add_printouts("Has creator", "Has license")

# Build the final query string
query_string = builder.build()

print(query_string)
# Output: [[Category:Programming languages]][[Has paradigm::Object-oriented]]|?Has creator|?Has license
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
from smw_reader import SMWClient, QueryBuilder

site = SMWClient("https://your-wiki.org/w/")
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

### Using Comparison Operators

The `QueryBuilder` supports various comparison operators for numerical and date properties.

- Greater than: `>...`
- Less than: `<...`
- Greater than or equal to: `>=...`
- Less than or equal to: `<=...`
- Not equal to: `!...`

Here is how to use these operators in your queries:

```python
from smw_reader import QueryBuilder

builder = QueryBuilder()

# Find pages with a population greater than 1,000,000
builder.add_conditions("Population:>1000000")
print(builder.build())
# Output: [[Population:>1000000]]

# Find pages with a creation date on or after January 1, 2024
builder = QueryBuilder()
builder.add_conditions("Creation date:>=2024-01-01")
print(builder.build())
# Output: [[Creation date:>=2024-01-01]]

# Combine multiple conditions, including a comparison
builder = QueryBuilder()
builder.add_conditions("Category:Cities", "Population:>=500000")
print(builder.build())
# Output: [[Category:Cities]][[Population:>=500000]]

### Passing Parameters

You can pass parameters like `limit`, `sort`, and `offset` directly to the `query` and `query_category` methods as keyword arguments.

#### With `query`

```python
from smw_reader import SMWClient

site = SMWClient("https://www.semantic-mediawiki.org/w/api.php")

# Execute a query with a limit of 5
results = site.ask.query("[[Category:Cities]]", limit=5)

print(results)
```

#### With `query_category`

You can also pass parameters to the `query_category` method:

```python
from smw_reader import SMWClient

site = SMWClient("https://www.semantic-mediawiki.org/w/api.php")

# Query the 'Cities' category with a limit of 3 and sort by population
results = site.ask.query_category(
    "Cities",
    printouts=["Population"],
    limit=3,
    sort="Population",
    order="desc"
)

print(results)
```
```