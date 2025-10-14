"""Custom exceptions for the SMW API client."""


class SMWAPIError(Exception):
    """Base exception for SMW API errors."""

    def __init__(self, message: str, status_code: int | None = None, response_data: dict | None = None) -> None:
        """Initialize SMW API error.

        Args:
            message: Error message.
            status_code: HTTP status code if available.
            response_data: Response data if available.
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class SMWConnectionError(SMWAPIError):
    """Exception raised when there's a connection error to the SMW API."""

    pass


class SMWAuthenticationError(SMWAPIError):
    """Exception raised when authentication fails."""

    pass


class SMWValidationError(SMWAPIError):
    """Exception raised when request parameters are invalid."""

    pass


class SMWServerError(SMWAPIError):
    """Exception raised when the SMW server returns an error."""

    pass
