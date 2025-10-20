"""Query builder for SMW queries."""

from typing import Self, Union


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
        condition_part = "".join(self.conditions)
        printout_part = "|".join(self.printouts)

        if condition_part and printout_part:
            return f"{condition_part}|{printout_part}"
        return condition_part or printout_part

    def __str__(self) -> str:
        """Return the string representation of the query.

        Returns:
            The formatted SMW query string.
        """
        return self.build()

    def add_conditions(self, *conditions: Union[str, dict[str, str]]) -> Self:
        """Add one or more conditions to the query.

        Args:
            *conditions: A list of conditions to add.
                Each condition can be a string or a dictionary.
                A string is treated as a raw condition, e.g. "Category:Test".
                A dict must contain 'key' and 'value', and optionally 'operator'.
                e.g. {"key": "Intro-Date", "operator": ">", "value": "2020-10-10"}

        Returns:
            The QueryBuilder instance for method chaining.
        """
        for condition in conditions:
            if isinstance(condition, str):
                self.conditions.append(f"[[{condition}]]")
            elif isinstance(condition, dict):
                key = condition.get("key")
                value = condition.get("value")
                if not key or value is None:
                    raise ValueError("Condition dictionary must contain 'key' and 'value'")

                operator = condition.get("operator", "")
                full_value = f"{operator}{value}"

                separator = ":" if str(key).lower() == "category" else "::"

                self.conditions.append(f"[[{key}{separator}{full_value}]]")
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
