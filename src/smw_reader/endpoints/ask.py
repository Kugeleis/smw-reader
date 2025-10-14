"""SMW API 'ask' endpoint implementation."""

from typing import Any, Dict, List, Optional, Union

from ..exceptions import SMWValidationError
from ..interfaces import APIEndpoint


class AskEndpoint(APIEndpoint):
    """Implementation of the SMW 'ask' API endpoint.

    The 'ask' endpoint allows executing semantic queries using SMW's query language.
    This endpoint supports the full semantic query syntax with conditions, printouts, and parameters.
    """

    @property
    def endpoint_name(self) -> str:
        """The name of the API endpoint."""
        return "ask"

    def execute(self, **params: Any) -> Dict[str, Any]:
        """Execute a semantic query using the 'ask' endpoint.

        Args:
            **params: Query parameters including:
                - query: The semantic query string (e.g., "[[Category:Person]]|?Name|?Age").
                - limit: Maximum number of results (default varies by wiki configuration)
                - offset: Offset for pagination
                - sort: Sort field
                - order: Sort order ('asc' or 'desc')
                - mainlabel: Label for the main result column
                - source: Source format

        Returns:
            The query results as a dictionary containing:
                - query: Query metadata
                - query-continue-offset: Offset for next page (if applicable)
                - results: Dictionary of result pages with properties
                - serializer: Serialization format information
                - version: SMW version information
                - meta: Additional metadata

        Raises:
            SMWValidationError: If the query is invalid.
            SMWAPIError: If the API request fails.
        """
        query = params.get("query")
        if not query or not isinstance(query, str):
            raise SMWValidationError("Query parameter must be a non-empty string")

        # Prepare request parameters
        request_params = {"query": query.strip()}

        # Add optional parameters
        for param_name, param_value in params.items():
            if param_name != "query" and param_value is not None:
                request_params[param_name] = param_value

        return self._client.make_request("ask", request_params)

    def ask(self, query: str, **params: Any) -> Dict[str, Any]:
        """Convenience method for executing semantic queries.

        Args:
            query: The semantic query string (e.g., "[[Category:Person]]|?Name|?Age").
            **params: Additional query parameters.

        Returns:
            The query results as a dictionary.
        """
        return self.execute(query=query, **params)

    def query_pages(
        self,
        conditions: List[str],
        printouts: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        mainlabel: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute a semantic query using structured parameters.

        This is a convenience method that builds the query string from structured parameters.

        Args:
            conditions: List of query conditions (e.g., ["[[Category:Person]]", "[[Age::>25]]"]).
            printouts: List of properties to include in results (e.g., ["?Name", "?Age"]).
            limit: Maximum number of results.
            offset: Offset for pagination.
            sort: Property to sort by.
            order: Sort order ('asc' or 'desc').
            mainlabel: Label for the main result column.

        Returns:
            The query results as a dictionary.

        Raises:
            SMWValidationError: If the parameters are invalid.
            SMWAPIError: If the API request fails.
        """
        if not conditions:
            raise SMWValidationError("At least one condition is required")

        # Build query string
        query_parts = conditions.copy()

        if printouts:
            query_parts.extend(printouts)

        query = "|".join(query_parts)

        # Prepare additional parameters
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort is not None:
            params["sort"] = sort
        if order is not None:
            if order.lower() not in ("asc", "desc"):
                raise SMWValidationError("Order must be 'asc' or 'desc'")
            params["order"] = order.lower()
        if mainlabel is not None:
            params["mainlabel"] = mainlabel

        return self.ask(query, **params)

    def query_concept(
        self,
        concept: str,
        printouts: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query pages belonging to a specific concept.

        Args:
            concept: The concept name (e.g., "Important People").
            printouts: List of properties to include in results.
            limit: Maximum number of results.
            offset: Offset for pagination.

        Returns:
            The query results as a dictionary.
        """
        conditions = [f"[[Concept:{concept}]]"]
        return self.query_pages(conditions=conditions, printouts=printouts, limit=limit, offset=offset)

    def query_category(
        self,
        category: str,
        printouts: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query pages in a specific category.

        Args:
            category: The category name (e.g., "People").
            printouts: List of properties to include in results.
            limit: Maximum number of results.
            offset: Offset for pagination.

        Returns:
            The query results as a dictionary.
        """
        conditions = [f"[[Category:{category}]]"]
        return self.query_pages(conditions=conditions, printouts=printouts, limit=limit, offset=offset)

    def query_property_value(
        self,
        property_name: str,
        value: Union[str, int, float],
        operator: str = "::",
        printouts: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query pages with a specific property value.

        Args:
            property_name: The property name.
            value: The property value to search for.
            operator: The comparison operator ("::", "::<", "::>", "::!", etc.).
            printouts: List of properties to include in results.
            limit: Maximum number of results.
            offset: Offset for pagination.

        Returns:
            The query results as a dictionary.
        """
        conditions = [f"[[{property_name}{operator}{value}]]"]
        return self.query_pages(conditions=conditions, printouts=printouts, limit=limit, offset=offset)
