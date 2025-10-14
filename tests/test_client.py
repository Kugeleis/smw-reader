"""Tests for SMW API client."""

from unittest.mock import Mock

import pytest

from smw_reader.client import SMWClient
from smw_reader.endpoints.ask import AskEndpoint
from smw_reader.exceptions import SMWAPIError, SMWValidationError


class TestSMWClient:
    """Test cases for SMWClient class."""

    @pytest.fixture
    def smw_client(self):
        """Create an SMWClient instance for testing."""
        return SMWClient("https://example.org/w/")

    def test_init(self, smw_client):
        """Test SMWClient initialization."""
        assert smw_client.base_url == "https://example.org/w/"
        assert smw_client.api_url == "https://example.org/w/api.php"
        assert hasattr(smw_client, "http_client")

    def test_init_with_custom_http_client(self):
        """Test SMWClient initialization with custom HTTP client."""
        mock_http_client = Mock()
        client = SMWClient("https://example.org/w/", http_client=mock_http_client)
        assert client.http_client == mock_http_client

    def test_init_with_custom_api_path(self):
        """Test SMWClient initialization with custom API path."""
        client = SMWClient("https://example.org/w/", api_path="custom/api.php")
        assert client.api_url == "https://example.org/w/custom/api.php"

    def test_url_normalization(self):
        """Test URL normalization in client initialization."""
        # Test with trailing slash
        client1 = SMWClient("https://example.org/w/")
        assert client1.base_url == "https://example.org/w/"

        # Test without trailing slash
        client2 = SMWClient("https://example.org/w")
        assert client2.base_url == "https://example.org/w/"

    def test_register_endpoint(self, smw_client):
        """Test registering an endpoint with the client."""
        mock_endpoint = Mock(spec=AskEndpoint)
        mock_endpoint.endpoint_name = "test"

        smw_client.register_endpoint(mock_endpoint)

        assert "test" in smw_client._endpoints
        assert smw_client._endpoints["test"] == mock_endpoint

    def test_get_endpoint_success(self, smw_client):
        """Test getting a registered endpoint."""
        mock_endpoint = Mock(spec=AskEndpoint)
        mock_endpoint.endpoint_name = "test"
        smw_client._endpoints["test"] = mock_endpoint

        result = smw_client.get_endpoint("test")

        assert result == mock_endpoint

    def test_get_endpoint_not_found(self, smw_client):
        """Test getting a non-existent endpoint raises error."""
        with pytest.raises(SMWValidationError) as exc_info:
            smw_client.get_endpoint("nonexistent")

        assert "Endpoint 'nonexistent' is not registered" in str(exc_info.value)

    def test_make_request_get_success(self, smw_client):
        """Test successful GET request."""
        mock_response = {"query": {"results": {}}}
        mock_http_client = Mock()
        mock_http_client.get.return_value = mock_response
        smw_client.http_client = mock_http_client

        result = smw_client.make_request("ask", {"query": "[[Category:Test]]"})

        assert result == mock_response
        mock_http_client.get.assert_called_once_with(
            smw_client.api_url,
            params={"action": "ask", "format": "json", "query": "[[Category:Test]]"},
        )

    def test_make_request_post_success(self, smw_client):
        """Test successful POST request."""
        mock_response = {"query": {"results": {}}}
        mock_http_client = Mock()
        mock_http_client.post.return_value = mock_response
        smw_client.http_client = mock_http_client

        result = smw_client.make_request("ask", {"query": "[[Category:Test]]"}, method="POST")

        assert result == mock_response
        mock_http_client.post.assert_called_once_with(
            smw_client.api_url,
            data={"action": "ask", "format": "json", "query": "[[Category:Test]]"},
        )

    def test_make_request_api_error(self, smw_client):
        """Test handling of API error responses."""
        error_response = {"error": {"code": "badquery", "info": "Invalid query syntax"}}
        mock_http_client = Mock()
        mock_http_client.get.return_value = error_response
        smw_client.http_client = mock_http_client

        with pytest.raises(SMWAPIError) as exc_info:
            smw_client.make_request("ask", {"query": "invalid"})

        assert "Invalid query syntax" in str(exc_info.value)
        assert exc_info.value.response_data == error_response["error"]

    def test_make_request_unsupported_method(self, smw_client):
        """Test handling of unsupported HTTP methods."""
        with pytest.raises(SMWValidationError) as exc_info:
            smw_client.make_request("ask", method="PUT")

        assert "Unsupported HTTP method: PUT" in str(exc_info.value)

    def test_make_request_http_exception(self, smw_client):
        """Test handling of HTTP client exceptions."""
        mock_http_client = Mock()
        mock_http_client.get.side_effect = Exception("Network error")
        smw_client.http_client = mock_http_client

        with pytest.raises(SMWAPIError) as exc_info:
            smw_client.make_request("ask")

        assert "Request failed: Network error" in str(exc_info.value)

    def test_make_request_no_params(self, smw_client):
        """Test request with no additional parameters."""
        mock_response = {"query": {"results": {}}}
        mock_http_client = Mock()
        mock_http_client.get.return_value = mock_response
        smw_client.http_client = mock_http_client

        result = smw_client.make_request("ask")

        assert result == mock_response
        mock_http_client.get.assert_called_once_with(
            smw_client.api_url, params={"action": "ask", "format": "json"}
        )
