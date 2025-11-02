"""SMW API 'ask' endpoint implementation."""

from typing import Any

from ..exceptions import SMWValidationError
from ..interfaces import APIEndpoint
from .query import QueryBuilder


class AskEndpoint(APIEndpoint):
    """Implementation of the SMW 'ask' API endpoint.

    The 'ask' endpoint allows executing semantic queries using SMW's query language.
    This endpoint supports the full semantic query syntax with conditions, printouts,
    and parameters.

    The recommended way to build complex queries is by using the `QueryBuilder`.
    See the `query` method for more details.
    """

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
                - p_...: Special parameters for 'Special:Ask' (e.g., p_limit=100)

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
            if param_name == "query" or param_value is None:
                continue

            if param_name.startswith("p_"):
                key = param_name[2:]
                request_params[f"p[{key}]"] = param_value
            else:
                request_params[param_name] = param_value

        return self._client.make_request("ask", request_params)

    def query(self, query: str | QueryBuilder, **params: Any) -> dict[str, Any]:
        """Convenience method for executing semantic queries.

        This method accepts either a raw SMW query string or a `QueryBuilder`
        instance, which allows for programmatic construction of queries.

        Examples:
            Using a raw query string:

            >>> site.ask.query("[[Category:Cities]]|?Population")

            Using the `QueryBuilder`:

            >>> from smw_reader import QueryBuilder
            >>> builder = QueryBuilder()
            >>> builder.add_conditions("Category:Cities").add_printouts("Population")
            >>> site.ask.query(builder)

        Args:
            query: The semantic query string or a QueryBuilder instance.
            **params: Additional query parameters.

        Returns:
            The query results as a dictionary.
        """
        return self.execute(query=str(query), **params)

    def query_category(self, category: str, printouts: list[str] | None = None, **params: Any) -> dict[str, Any]:
        """Query pages in a specific category.

        This is a convenience method that builds and executes a query for a given
        category.

        Args:
            category: The name of the category to query.
            printouts: A list of properties to retrieve for each page.
            **params: Additional query parameters.

        Returns:
            The query results as a dictionary.
        """
        query_builder = QueryBuilder().add_conditions(f"Category:{category}")
        if printouts:
            # The query builder expects printouts without the '?' prefix.
            clean_printouts = [p.lstrip("?") for p in printouts]
            query_builder.add_printouts(*clean_printouts)
        return self.query(query_builder, **params)
