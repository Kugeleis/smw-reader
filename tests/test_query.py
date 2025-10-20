"""Tests for SMW QueryBuilder."""

import pytest

from smw_reader.endpoints.query import QueryBuilder


class TestQueryBuilder:
    """Test cases for QueryBuilder class."""

    def test_build_simple_query(self):
        """Test building a simple query."""
        query = QueryBuilder().add_conditions("Category:Test").build()
        assert query == "[[Category:Test]]"

    def test_build_query_with_printouts(self):
        """Test building a query with printouts."""
        query = QueryBuilder().add_conditions("Category:Test").add_printouts("Name", "Age").build()
        assert query == "[[Category:Test]]|?Name|?Age"

    def test_build_empty_query(self):
        """Test building an empty query."""
        query = QueryBuilder().build()
        assert query == ""

    def test_str_representation(self):
        """Test the string representation of the QueryBuilder."""
        query_builder = QueryBuilder().add_conditions("Category:Test")
        assert str(query_builder) == "[[Category:Test]]"

    def test_add_condition_with_dict(self):
        """Test adding a condition using a dictionary."""
        query = QueryBuilder().add_conditions(
            {"key": "Intro-Date", "operator": ">", "value": "2020-10-10"}
        ).build()
        assert query == "[[Intro-Date::>2020-10-10]]"

    def test_add_condition_with_category_dict(self):
        """Test adding a category condition using a dictionary."""
        query = QueryBuilder().add_conditions(
            {"key": "Category", "value": "Test"}
        ).build()
        assert query == "[[Category:Test]]"

    def test_add_multiple_conditions(self):
        """Test adding multiple conditions."""
        query = QueryBuilder().add_conditions(
            "Category:Test",
            {"key": "Intro-Date", "operator": ">", "value": "2020-10-10"}
        ).build()
        assert query == "[[Category:Test]][[Intro-Date::>2020-10-10]]"

    def test_add_condition_with_no_operator(self):
        """Test adding a condition with no operator."""
        query = QueryBuilder().add_conditions(
            {"key": "Name", "value": "Test"}
        ).build()
        assert query == "[[Name::Test]]"

    def test_add_condition_invalid_dict(self):
        """Test that adding an invalid dictionary raises an error."""
        with pytest.raises(ValueError):
            QueryBuilder().add_conditions({"key": "Name"})

    def test_add_condition_with_multiple_printouts(self):
        """Test adding multiple printouts."""
        query = QueryBuilder().add_printouts("Name", "Age", "Location").build()
        assert query == "?Name|?Age|?Location"

    def test_complex_query(self):
        """Test a complex query with multiple conditions and printouts."""
        query = QueryBuilder().add_conditions(
            "Category:FRITZ!Box-Family",
            {"key": "Intro-Date", "operator": ">", "value": "#time:2020-10-10"}
        ).add_printouts(
            "Name", "Age"
        ).build()
        expected = "[[Category:FRITZ!Box-Family]][[Intro-Date::>#time:2020-10-10]]|?Name|?Age"
        assert query == expected

    def test_build_query_with_multiple_dict_conditions(self):
        """Test building a query with multiple dictionary conditions."""
        query = QueryBuilder().add_conditions(
            {"key": "Category", "value": "Test"},
            {"key": "Status", "value": "Active"}
        ).build()
        assert query == "[[Category:Test]][[Status::Active]]"
