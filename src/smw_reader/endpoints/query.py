"""Query builder for SMW queries."""

from typing import Self


class QueryBuilder:
    """A fluent interface for building complex SMW queries.

    This class allows for the programmatic construction of query strings by chaining
    methods to add conditions and printouts.

    Attributes:
        conditions: A list of query conditions (e.g., "[[Category:Person]]").
        printouts: A list of properties to print (e.g., "?Name").
    """

    def __init__(self) -> None:
        """Initialize a new QueryBuilder instance."""
        self.conditions: list[str] = []
        self.printouts: list[str] = []

    def build(self) -> str:
        """Build the final query string by joining conditions and printouts.

        Returns:
            The formatted SMW query string.
        """
        return "|".join(self.conditions + self.printouts)

    def __str__(self) -> str:
        """Return the string representation of the query.

        Returns:
            The formatted SMW query string.
        """
        return self.build()

    def add_conditions(self, *conditions: str) -> Self:
        """Add one or more conditions to the query.

        Args:
            *conditions: A list of conditions to add.

        Returns:
            The QueryBuilder instance for method chaining.
        """
        self.conditions.extend(f"[[{c}]]" for c in conditions)
        return self

    def add_printouts(self, *printouts: str) -> Self:
        """Add one or more printouts to the query.

        Args:
            *printouts: A list of printouts to add.

        Returns:
            The QueryBuilder instance for method chaining.
        """
        self.printouts.extend(f"?{p}" for p in printouts)
        return self
