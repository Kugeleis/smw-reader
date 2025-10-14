"""Tests for SMW API client exceptions."""

from smw_reader.exceptions import (
    SMWAPIError,
    SMWAuthenticationError,
    SMWConnectionError,
    SMWServerError,
    SMWValidationError,
)


def test_smw_api_error_basic():
    """Test basic SMW API error creation."""
    error = SMWAPIError("Test error")
    assert str(error) == "Test error"
    assert error.status_code is None
    assert error.response_data is None


def test_smw_api_error_with_details():
    """Test SMW API error with status code and response data."""
    response_data = {"code": "test", "info": "Test error"}
    error = SMWAPIError("Test error", status_code=400, response_data=response_data)

    assert str(error) == "Test error"
    assert error.status_code == 400
    assert error.response_data == response_data


def test_smw_connection_error():
    """Test SMW connection error inheritance."""
    error = SMWConnectionError("Connection failed")
    assert isinstance(error, SMWAPIError)
    assert str(error) == "Connection failed"


def test_smw_authentication_error():
    """Test SMW authentication error inheritance."""
    error = SMWAuthenticationError("Auth failed")
    assert isinstance(error, SMWAPIError)
    assert str(error) == "Auth failed"


def test_smw_validation_error():
    """Test SMW validation error inheritance."""
    error = SMWValidationError("Invalid params")
    assert isinstance(error, SMWAPIError)
    assert str(error) == "Invalid params"


def test_smw_server_error():
    """Test SMW server error inheritance."""
    error = SMWServerError("Server error")
    assert isinstance(error, SMWAPIError)
    assert str(error) == "Server error"
