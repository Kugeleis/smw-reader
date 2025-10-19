# Semantic MediaWiki (SMW) Query Syntax

This document provides a guide to the SMW query syntax used in this library, with examples for each of the available methods in the `AskEndpoint` class.

## `query_dict`: Composing Queries with a Dictionary

The `query_dict` method allows you to build complex SMW queries using a structured dictionary.

**Method Signature:**

```python
def query_dict(
    self,
    query_conditions: dict[str, Any],
    printouts: list[str] | None = None,
    # ... other optional parameters
) -> dict[str, Any]:
```

### `query_conditions` Dictionary Structure:

- **`categories`**: A list of category names to include in the query.
  - Example: `["Free-Software"]`
- **`concepts`**: A list of concept names.
  - Example: `["Users"]`
- **`properties`**: A dictionary where keys are property names and values define the condition.
  - **Simple equality**: `{"Modification date": "2020-10-10"}`
  - **With operator**: `{"Modification date": {"value": ">2020-10-10", "operator": "::"}}`

### Example:

```python
query_conditions = {
    "categories": ["Free-Software"],
    "properties": {
        "Modification date": {"value": "2020-10-10", "operator": "::>"},
    },
}
ask_endpoint.query_dict(query_conditions)
```

This generates the SMW query: `[[Category:Free-Software]][[Modification date::>2020-10-10]]`

## Existing `query_*` Methods

Here are examples for the other query methods available in `AskEndpoint`.

### `query_pages`

Builds a query from a list of raw condition strings.

**Example:**

```python
ask_endpoint.query_pages(
    conditions=["[[Category:Free-Software]]", "[[Modification date::>2020-10-10]]"],
    printouts=["?Modification date"]
)
```

### `query_category`

Queries for pages within a specific category.

**Example:**

```python
ask_endpoint.query_category(
    category="Free-Software",
    printouts=["?Modification date"]
)
```

### `query_concept`

Queries for pages belonging to a specific concept.

**Example:**

```python
ask_endpoint.query_concept(
    concept="Users",
    printouts=["?Name"]
)
```

### `query_property_value`

Queries for pages where a property matches a specific value, with an optional operator.

**Example:**

```python
ask_endpoint.query_property_value(
    property_name="Modification date",
    value="2020-10-10",
    operator="::>",
    printouts=["?Modification date"]
)
```
