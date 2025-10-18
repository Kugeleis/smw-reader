"""SMW API 'ask' endpoint implementation."""

import warnings
from typing import Any

from ..exceptions import SMWValidationError
from ..interfaces import APIEndpoint
from .query import QueryBuilder


class AskEndpoint(APIEndpoint):
    """Implementation of the SMW 'ask' API endpoint.

    The 'ask' endpoint allows executing semantic queries using SMW's query language.
    This endpoint supports the full semantic query syntax with conditions, printouts,
    and parameters.
    """

    def _format_printouts(self, printouts: list[str] | None) -> list[str] | None:
        if not printouts:
            return printouts
        return [f"?{p}" if not p.startswith("?") else p for p in printouts]

    @property
    def endpoint_name(self) -> str:
        """The name of the API endpoint."""
        return "ask"

    def execute(self, **params: Any) -> dict[str, Any]:
        """Execute a semantic query using the 'ask' endpoint.

        Args:
            **params: Query parameters including:
                - query: The semantic query string
                - limit: Maximum number of results
                - offset: Offset for pagination
                - sort: Sort field
                - order: Sort order ('asc' or 'desc')

        Returns:
            The query results as a dictionary.

        Raises:
            SMWValidationError: If the query is invalid.
        """
        query = params.get("query")
        if not query or not isinstance(query, str):
            raise SMWValidationError("Query parameter must be a non-empty string")

        request_params = {"query": query.strip()}
        for param_name, param_value in params.items():
            if param_name != "query" and param_value is not None:
                request_params[param_name] = param_value

        return self._client.make_request("ask", request_params)

    def query(self, query: str | QueryBuilder, **params: Any) -> dict[str, Any]:
        """Convenience method for executing semantic queries.

        Args:
            query: The semantic query string or a QueryBuilder instance.
            **params: Additional query parameters.

        Returns:
            The query results as a dictionary.
        """
        return self.execute(query=str(query), **params)

    def ask(self, query: str | QueryBuilder, **params: Any) -> dict[str, Any]:
        """Alias for the query method."""
        warnings.warn(
            "The 'ask' method is deprecated, use 'query' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.query(query, **params)

    def query_pages(
        self, conditions: list[str], printouts: list[str] | None = None, **params: Any
    ) -> dict[str, Any]:
        """Execute a semantic query using structured parameters."""
        warnings.warn(
            "The 'query_pages' method is deprecated.", DeprecationWarning, stacklevel=2
        )
        if not conditions:
            raise SMWValidationError("At least one condition is required")
        query_parts = conditions.copy()
        if printouts:
            query_parts.extend(printouts)
        return self.query("|".join(query_parts), **params)

    def query_concept(
        self, concept: str, printouts: list[str] | None = None, **params: Any
    ) -> dict[str, Any]:
        """Query pages belonging to a specific concept."""
        warnings.warn(
            "The 'query_concept' method is deprecated.", DeprecationWarning, stacklevel=2
        )
        return self.query_pages(
            [f"[[Concept:{concept}]]"], self._format_printouts(printouts), **params
        )

    def query_category(
        self, category: str, printouts: list[str] | None = None, **params: Any
    ) -> dict[str, Any]:
        """Query pages in a specific category."""
        warnings.warn(
            "The 'query_category' method is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.query_pages(
            [f"[[Category:{category}]]"], self._format_printouts(printouts), **params
        )

    def query_property_value(
        self,
        property_name: str,
        value: Any,
        operator: str = "::",
        printouts: list[str] | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        """Query pages with a specific property value."""
        warnings.warn(
            "The 'query_property_value' method is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.query_pages(
            [f"[[{property_name}{operator}{value}]]"],
            self._format_printouts(printouts),
            **params,
        )

    def query_dict(
        self, query_conditions: dict[str, Any], printouts: list[str] | None = None, **params: Any
    ) -> dict[str, Any]:
        """Execute a semantic query using a dictionary of conditions."""
        warnings.warn(
            "The 'query_dict' method is deprecated.", DeprecationWarning, stacklevel=2
        )
        conditions = []
        if "categories" in query_conditions:
            if not isinstance(query_conditions["categories"], list):
                raise SMWValidationError("'categories' must be a list of strings.")
            for category in query_conditions["categories"]:
                conditions.append(f"[[Category:{category}]]")
        if "concepts" in query_conditions:
            if not isinstance(query_conditions["concepts"], list):
                raise SMWValidationError("'concepts' must be a list of strings.")
            for concept in query_conditions["concepts"]:
                conditions.append(f"[[Concept:{concept}]]")
        if "properties" in query_conditions:
            if not isinstance(query_conditions["properties"], dict):
                raise SMWValidationError("'properties' must be a dictionary.")
            for prop, value_or_dict in query_conditions["properties"].items():
                if isinstance(value_or_dict, dict):
                    operator = value_or_dict.get("operator", "::")
                    value = value_or_dict.get("value")
                    if value is None:
                        raise SMWValidationError(f"Property '{prop}' dictionary must have a 'value' key.")
                    conditions.append(f"[[{prop}{operator}{value}]]")
                else:
                    conditions.append(f"[[{prop}::{value_or_dict}]]")
        return self.query_pages(conditions, self._format_printouts(printouts), **params)
