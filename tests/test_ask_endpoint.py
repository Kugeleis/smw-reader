"""Tests for SMW Ask endpoint."""

from unittest.mock import Mock

import pytest

from smw_reader.endpoints.ask import AskEndpoint, QueryBuilder
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
        ask_endpoint._client.make_request.return_value = {}
        result = ask_endpoint.execute(query="[[Category:Test]]")
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with("ask", {"query": "[[Category:Test]]"})

    def test_execute_empty_query_raises_error(self, ask_endpoint):
        """Test that empty query raises validation error."""
        with pytest.raises(SMWValidationError):
            ask_endpoint.execute(query="")

    def test_query_with_string(self, ask_endpoint):
        """Test the query method with a string."""
        ask_endpoint._client.make_request.return_value = {}
        result = ask_endpoint.query("[[Category:Test]]")
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with("ask", {"query": "[[Category:Test]]"})

    def test_query_with_parameters(self, ask_endpoint):
        """Test the query method with additional parameters."""
        ask_endpoint._client.make_request.return_value = {}
        result = ask_endpoint.query("[[Category:Test]]", limit=10, sort="Name")
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]|limit=10|sort=Name"}
        )

    def test_query_with_query_builder(self, ask_endpoint):
        """Test the query method with a QueryBuilder instance."""
        ask_endpoint._client.make_request.return_value = {}
        query = QueryBuilder().add_conditions({"key": "Category", "value": "Test"})
        result = ask_endpoint.query(query)
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with("ask", {"query": "[[Category:Test]]"})

    def test_query_category(self, ask_endpoint):
        """Test the query_category method."""
        ask_endpoint._client.make_request.return_value = {}
        result = ask_endpoint.query_category("Test")
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with("ask", {"query": "[[Category:Test]]"})

    def test_query_category_with_printouts(self, ask_endpoint):
        """Test the query_category method with printouts."""
        ask_endpoint._client.make_request.return_value = {}
        result = ask_endpoint.query_category("Test", printouts=["Name", "?Age"])
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with("ask", {"query": "[[Category:Test]]|?Name|?Age"})
