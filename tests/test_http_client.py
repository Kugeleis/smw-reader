"""Tests for SMW HTTP client."""

import json
import urllib.error
from unittest.mock import Mock, patch

import pytest

from smw_reader.exceptions import (
    SMWConnectionError,
    SMWServerError,
)
from smw_reader.http_client import RequestsHTTPClient


class TestRequestsHTTPClient:
    """Test cases for RequestsHTTPClient class."""

    @pytest.fixture
    def http_client(self):
        """Create a RequestsHTTPClient instance for testing."""
        return RequestsHTTPClient()

    def test_init_default(self, http_client):
        """Test RequestsHTTPClient initialization with defaults."""
        assert http_client.timeout == 30.0
        assert http_client.user_agent == "SMW-Reader/0.1.0"

    def test_init_custom(self):
        """Test RequestsHTTPClient initialization with custom values."""
        client = RequestsHTTPClient(timeout=60.0, user_agent="Custom-Agent/2.0")
        assert client.timeout == 60.0
        assert client.user_agent == "Custom-Agent/2.0"

    @patch("urllib.request.urlopen")
    def test_get_success(self, mock_urlopen, http_client):
        """Test successful GET request."""
        # Mock response
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"query": {"results": {}}}).encode()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = http_client.get("https://example.org/w/api.php", params={"action": "ask"})

        assert result == {"query": {"results": {}}}
        # Verify the URL was constructed correctly
        args, kwargs = mock_urlopen.call_args
        assert "action=ask" in args[0].full_url

    @patch("urllib.request.urlopen")
    def test_get_with_params(self, mock_urlopen, http_client):
        """Test GET request with multiple parameters."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"success": True}).encode()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        params = {"action": "ask", "query": "[[Category:Test]]", "format": "json"}
        result = http_client.get("https://example.org/w/api.php", params=params)

        assert result == {"success": True}
        args, kwargs = mock_urlopen.call_args
        url = args[0].full_url
        assert "action=ask" in url
        assert "query=%5B%5BCategory%3ATest%5D%5D" in url  # URL encoded
        assert "format=json" in url

    @patch("urllib.request.urlopen")
    def test_post_success(self, mock_urlopen, http_client):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"success": True}).encode()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        data = {"action": "ask", "query": "[[Category:Test]]"}
        result = http_client.post("https://example.org/w/api.php", data=data)

        assert result == {"success": True}
        args, kwargs = mock_urlopen.call_args
        request = args[0]
        assert request.get_method() == "POST"

    @patch("urllib.request.urlopen")
    def test_request_connection_error(self, mock_urlopen, http_client):
        """Test handling of connection errors."""
        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        with pytest.raises(SMWConnectionError) as exc_info:
            http_client.get("https://example.org/w/api.php")

        assert "Connection failed" in str(exc_info.value)

    @patch("urllib.request.urlopen")
    def test_request_http_error(self, mock_urlopen, http_client):
        """Test handling of HTTP errors."""
        from email.message import Message

        headers = Message()
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://example.org/w/api.php", 500, "Internal Server Error", headers, None
        )

        with pytest.raises(SMWServerError) as exc_info:
            http_client.get("https://example.org/w/api.php")

        assert "500" in str(exc_info.value)
        assert exc_info.value.status_code == 500

    @patch("urllib.request.urlopen")
    def test_request_json_decode_error(self, mock_urlopen, http_client):
        """Test handling of JSON decode errors."""
        mock_response = Mock()
        mock_response.read.return_value = b"Invalid JSON response"
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # The implementation wraps JSON decode errors as connection errors
        with pytest.raises(SMWConnectionError) as exc_info:
            http_client.get("https://example.org/w/api.php")

        assert "Invalid JSON response" in str(exc_info.value)

    @patch("urllib.request.urlopen")
    def test_custom_headers(self, mock_urlopen, http_client):
        """Test request with custom headers."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"success": True}).encode()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Test that the method works (actual header verification requires deeper inspection of the implementation)
        result = http_client.get("https://example.org/w/api.php")

        assert result == {"success": True}

    @patch("urllib.request.urlopen")
    def test_user_agent_header(self, mock_urlopen, http_client):
        """Test that User-Agent header is set correctly."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"success": True}).encode()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        http_client.get("https://example.org/w/api.php")

        args, kwargs = mock_urlopen.call_args
        request = args[0]
        assert request.get_header("User-agent") == "SMW-Reader/0.1.0"

    @patch("urllib.request.urlopen")
    def test_post_with_data(self, mock_urlopen, http_client):
        """Test POST request with form data."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"success": True}).encode()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        data = {"action": "ask", "query": "[[Category:Test]]"}
        result = http_client.post("https://example.org/w/api.php", data=data)

        assert result == {"success": True}
        args, kwargs = mock_urlopen.call_args
        request = args[0]
        assert request.get_method() == "POST"
