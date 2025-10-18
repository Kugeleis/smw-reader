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
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]"}
        )

    def test_execute_empty_query_raises_error(self, ask_endpoint):
        """Test that empty query raises validation error."""
        with pytest.raises(SMWValidationError):
            ask_endpoint.execute(query="")

    def test_query_with_string(self, ask_endpoint):
        """Test the query method with a string."""
        ask_endpoint._client.make_request.return_value = {}
        result = ask_endpoint.query("[[Category:Test]]")
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]"}
        )

    def test_query_with_parameters(self, ask_endpoint):
        """Test the query method with additional parameters."""
        ask_endpoint._client.make_request.return_value = {}
        result = ask_endpoint.query("[[Category:Test]]", limit=10, sort="Name")
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]", "limit": 10, "sort": "Name"}
        )

    def test_query_with_query_builder(self, ask_endpoint):
        """Test the query method with a QueryBuilder instance."""
        ask_endpoint._client.make_request.return_value = {}
        query = QueryBuilder().add_conditions("Category:Test")
        result = ask_endpoint.query(query)
        assert result == {}
        ask_endpoint._client.make_request.assert_called_once_with(
            "ask", {"query": "[[Category:Test]]"}
        )

    def test_ask_method_deprecation_warning(self, ask_endpoint):
        """Test that the ask method raises a DeprecationWarning."""
        with pytest.deprecated_call():
            ask_endpoint.ask("[[Category:Test]]")

    def test_deprecated_methods_warnings_and_functionality(self, ask_endpoint):
        """Test that deprecated methods raise warnings and are functional."""
        with pytest.deprecated_call():
            ask_endpoint.query_pages(["[[Category:Test]]"])
        with pytest.deprecated_call():
            ask_endpoint.query_concept("Test")
        with pytest.deprecated_call():
            ask_endpoint.query_category("Test")
        with pytest.deprecated_call():
            ask_endpoint.query_property_value("Prop", "Val")
        with pytest.deprecated_call():
            ask_endpoint.query_dict({"categories": ["Test"]})

    def test_query_dict_invalid_inputs(self, ask_endpoint):
        """Test query_dict with invalid inputs."""
        with pytest.raises(SMWValidationError):
            ask_endpoint.query_dict({"categories": "not-a-list"})
        with pytest.raises(SMWValidationError):
            ask_endpoint.query_dict({"concepts": "not-a-list"})
        with pytest.raises(SMWValidationError):
            ask_endpoint.query_dict({"properties": "not-a-dict"})
        with pytest.raises(SMWValidationError):
            ask_endpoint.query_dict({"properties": {"prop": {"operator": "::"}}})


class TestQueryBuilder:
    """Test cases for QueryBuilder class."""

    def test_build_simple_query(self):
        """Test building a simple query."""
        query = QueryBuilder().add_conditions("Category:Test").build()
        assert query == "[[Category:Test]]"

    def test_build_query_with_printouts(self):
        """Test building a query with printouts."""
        query = (
            QueryBuilder()
            .add_conditions("Category:Test")
            .add_printouts("Name", "Age")
            .build()
        )
        assert query == "[[Category:Test]]|?Name|?Age"

    def test_build_empty_query(self):
        """Test building an empty query."""
        query = QueryBuilder().build()
        assert query == ""

    def test_str_representation(self):
        """Test the string representation of the QueryBuilder."""
        query_builder = QueryBuilder().add_conditions("Category:Test")
        assert str(query_builder) == "[[Category:Test]]"
