"""Test for SMW extension detection and error handling."""

from unittest.mock import Mock

import pytest

from smw_reader import SMWClient
from smw_reader.endpoints.ask import AskEndpoint
from smw_reader.exceptions import SMWAPIError


def test_smw_extension_missing_error():
    """Test handling of missing SMW extension error."""
    # Create client with mock HTTP client
    mock_http_client = Mock()
    client = SMWClient("https://example.com/w/", http_client=mock_http_client)

    # Mock the response for missing SMW extension
    mock_http_client.get.return_value = {
        "error": {
            "code": "badvalue",
            "info": 'Unrecognized value for parameter "action": ask.',
            "*": "See https://en.wikipedia.org/w/api.php for API usage.",
        }
    }

    # This should raise an SMWAPIError
    with pytest.raises(SMWAPIError) as exc_info:
        client.make_request("ask", {"query": "[[Category:Test]]"})

    # Verify error message
    assert "Unrecognized value for parameter" in str(exc_info.value)
    assert exc_info.value.response_data["code"] == "badvalue"


def test_ask_endpoint_with_missing_smw():
    """Test AskEndpoint behavior when SMW is not available."""
    # Create client and endpoint
    mock_http_client = Mock()
    client = SMWClient("https://example.com/w/", http_client=mock_http_client)
    ask_endpoint = AskEndpoint(client)

    # Mock the SMW missing error
    mock_http_client.get.return_value = {
        "error": {
            "code": "badvalue",
            "info": 'Unrecognized value for parameter "action": ask.',
        }
    }

    # Should propagate the error from the client
    with pytest.raises(SMWAPIError):
        ask_endpoint.ask("[[Category:Test]]")


if __name__ == "__main__":
    pytest.main([__file__])
