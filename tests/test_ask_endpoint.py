"""Tests for SMW Ask endpoint."""

from unittest.mock import Mock

import pytest

from smw_reader.endpoints.ask import AskEndpoint
from smw_reader.exceptions import SMWValidationError


class TestAskEndpoint:
    """Test cases for AskEndpoint class."""

    @pytest.fixture
    def ask_endpoint(self):
        """Create an AskEndpoint instance for testing."""
        mock_client = Mock()
        return AskEndpoint(mock_client)

    def test_endpoint_name(self, ask_endpoint):
        """Test endpoint name property."""
        assert ask_endpoint.endpoint_name == "ask"

    def test_execute_basic_query(self, ask_endpoint):
        """Test executing a basic semantic query."""
        mock_response = {
            "query": {
                "results": {
                    "TestPage": {
                        "printouts": {},
                        "fulltext": "TestPage",
                        "fullurl": "https://example.org/wiki/TestPage",
                    }
                }
            }
        }

        ask_endpoint._client.make_request.return_value = mock_response

        result = ask_endpoint.execute(query="[[Category:Test]]")

        assert result == mock_response
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]"}
        )

    def test_execute_query_with_parameters(self, ask_endpoint):
        """Test executing a query with additional parameters."""
        mock_response = {"query": {"results": {}}}
        ask_endpoint._client.make_request.return_value = mock_response

        result = ask_endpoint.execute(
            query="[[Category:Person]]|?Name|?Age",
            limit=10,
            offset=5,
            sort="Name",
            order="asc",
        )

        assert result == mock_response
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask",
            {
                "query": "[[Category:Person]]|?Name|?Age",
                "limit": 10,
                "offset": 5,
                "sort": "Name",
                "order": "asc",
            },
        )

    def test_execute_empty_query_raises_error(self, ask_endpoint):
        """Test that empty query raises validation error."""
        with pytest.raises(SMWValidationError) as exc_info:
            ask_endpoint.execute(query="")

        assert "Query parameter must be a non-empty string" in str(exc_info.value)

    def test_execute_none_query_raises_error(self, ask_endpoint):
        """Test that None query raises validation error."""
        with pytest.raises(SMWValidationError) as exc_info:
            ask_endpoint.execute(query=None)

        assert "Query parameter must be a non-empty string" in str(exc_info.value)

    def test_execute_non_string_query_raises_error(self, ask_endpoint):
        """Test that non-string query raises validation error."""
        with pytest.raises(SMWValidationError) as exc_info:
            ask_endpoint.execute(query=123)

        assert "Query parameter must be a non-empty string" in str(exc_info.value)

    def test_execute_missing_query_raises_error(self, ask_endpoint):
        """Test that missing query parameter raises validation error."""
        with pytest.raises(SMWValidationError) as exc_info:
            ask_endpoint.execute(limit=10)

        assert "Query parameter must be a non-empty string" in str(exc_info.value)

    def test_ask_method(self, ask_endpoint):
        """Test the convenience ask method."""
        mock_response = {"query": {"results": {}}}
        ask_endpoint._client.make_request.return_value = mock_response

        result = ask_endpoint.ask("[[Category:Test]]")

        assert result == mock_response
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]"}
        )

    def test_ask_method_with_kwargs(self, ask_endpoint):
        """Test the ask method with additional keyword arguments."""
        mock_response = {"query": {"results": {}}}
        ask_endpoint._client.make_request.return_value = mock_response

        result = ask_endpoint.ask("[[Category:Test]]", limit=5, sort="Title")

        assert result == mock_response
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]", "limit": 5, "sort": "Title"}
        )

    def test_ask_with_printouts(self, ask_endpoint):
        """Test asking with printout statements."""
        query_with_printouts = "[[Category:Person]]|?Name|?Age|?City"
        mock_response = {
            "query": {
                "results": {
                    "John Doe": {
                        "printouts": {
                            "Name": ["John Doe"],
                            "Age": [30],
                            "City": ["New York"],
                        }
                    }
                }
            }
        }
        ask_endpoint._client.make_request.return_value = mock_response

        result = ask_endpoint.ask(query_with_printouts)

        assert result == mock_response
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": query_with_printouts}
        )

    def test_ask_with_conditions_and_sorting(self, ask_endpoint):
        """Test complex query with conditions and sorting."""
        complex_query = "[[Category:Person]][[Age::>25]]|?Name|?Age|sort=Age|order=desc|limit=10"
        mock_response = {"query": {"results": {}}}
        ask_endpoint._client.make_request.return_value = mock_response

        result = ask_endpoint.ask(complex_query)

        assert result == mock_response
        ask_endpoint._client.make_request.assert_called_once_with("ask", {"query": complex_query})

    def test_endpoint_inheritance(self, ask_endpoint):
        """Test that AskEndpoint properly inherits from APIEndpoint."""
        from smw_reader.interfaces import APIEndpoint

        assert isinstance(ask_endpoint, APIEndpoint)
        assert hasattr(ask_endpoint, "_client")
        assert hasattr(ask_endpoint, "execute")
        assert hasattr(ask_endpoint, "endpoint_name")

    def test_build_conditions_static_method(self):
        """Test the build_conditions static method."""
        conditions = ["Category:Software", "License::GPL", "Age::>25"]
        expected = ["[[Category:Software]]", "[[License::GPL]]", "[[Age::>25]]"]

        result = AskEndpoint.build_conditions(conditions)

        assert result == expected

    def test_build_conditions_empty_list(self):
        """Test build_conditions with empty list."""
        conditions = []
        expected = []

        result = AskEndpoint.build_conditions(conditions)

        assert result == expected

    def test_build_conditions_single_item(self):
        """Test build_conditions with single condition."""
        conditions = ["Category:Test"]
        expected = ["[[Category:Test]]"]

        result = AskEndpoint.build_conditions(conditions)

        assert result == expected

    def test_build_conditions_complex_conditions(self):
        """Test build_conditions with complex semantic conditions."""
        conditions = [
            "Category:Person",
            "Age::>25",
            "City::New York",
            "Has friend.Category:Developer",
        ]
        expected = [
            "[[Category:Person]]",
            "[[Age::>25]]",
            "[[City::New York]]",
            "[[Has friend.Category:Developer]]",
        ]

        result = AskEndpoint.build_conditions(conditions)

        assert result == expected

    def test_build_printouts_static_method(self):
        """Test the build_printouts static method."""
        printouts = ["Name", "License", "Homepage URL"]
        expected = ["?Name", "?License", "?Homepage URL"]

        result = AskEndpoint.build_printouts(printouts)

        assert result == expected

    def test_build_printouts_empty_list(self):
        """Test build_printouts with empty list."""
        printouts = []
        expected = []

        result = AskEndpoint.build_printouts(printouts)

        assert result == expected

    def test_build_printouts_single_item(self):
        """Test build_printouts with single printout."""
        printouts = ["Name"]
        expected = ["?Name"]

        result = AskEndpoint.build_printouts(printouts)

        assert result == expected

    def test_build_printouts_complex_properties(self):
        """Test build_printouts with complex semantic properties."""
        printouts = ["Name", "Has friend.Name", "Located in.Population", "Creation date"]
        expected = ["?Name", "?Has friend.Name", "?Located in.Population", "?Creation date"]

        result = AskEndpoint.build_printouts(printouts)

        assert result == expected

    def test_build_conditions_instance_method(self, ask_endpoint):
        """Test that build_conditions works as instance method too."""
        conditions = ["Category:Test"]
        expected = ["[[Category:Test]]"]

        result = ask_endpoint.build_conditions(conditions)

        assert result == expected

    def test_build_printouts_instance_method(self, ask_endpoint):
        """Test that build_printouts works as instance method too."""
        printouts = ["Name", "Age"]
        expected = ["?Name", "?Age"]

        result = ask_endpoint.build_printouts(printouts)

        assert result == expected

    def test_utility_methods_integration_with_query_pages(self, ask_endpoint):
        """Test that utility methods integrate properly with query_pages."""
        mock_response = {"query": {"results": {}}}
        ask_endpoint._client.make_request.return_value = mock_response

        # Use utility methods to build query components
        conditions = AskEndpoint.build_conditions(["Category:Person", "Age::>25"])
        printouts = AskEndpoint.build_printouts(["Name", "Age"])

        # This should work with query_pages method
        result = ask_endpoint.query_pages(conditions=conditions, printouts=printouts, limit=10)

        expected_query = "[[Category:Person]]|[[Age::>25]]|?Name|?Age"
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": expected_query, "limit": 10}
        )
        assert result == mock_response
