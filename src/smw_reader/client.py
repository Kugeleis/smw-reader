"""Main SMW API client implementation."""

from typing import Any
from urllib.parse import urljoin

from .exceptions import SMWAPIError, SMWValidationError
from .http_client import RequestsHTTPClient
from .interfaces import APIEndpoint, HTTPClient


class SMWClient:
    """Main client for accessing Semantic MediaWiki API.

    This client provides a modular interface to various SMW API endpoints
    following dependency injection and open/closed principles.
    """

    def __init__(
        self,
        base_url: str,
        http_client: HTTPClient | None = None,
        api_path: str = "api.php",
    ) -> None:
        """Initialize the SMW client.

        Args:
            base_url: Base URL of the MediaWiki installation (e.g., "https://example.com/wiki/").
            http_client: HTTP client instance. If None, uses default RequestsHTTPClient.
            api_path: Path to the API endpoint (default: "api.php").
        """
        self.base_url = base_url.rstrip("/") + "/"
        self.api_url = urljoin(self.base_url, api_path)
        self.http_client = http_client or RequestsHTTPClient()
        self._endpoints: dict[str, APIEndpoint] = {}

    def register_endpoint(self, endpoint: APIEndpoint) -> None:
        """Register an API endpoint with the client.

        Args:
            endpoint: The endpoint instance to register.
        """
        self._endpoints[endpoint.endpoint_name] = endpoint

    def get_endpoint(self, name: str) -> APIEndpoint:
        """Get a registered endpoint by name.

        Args:
            name: The endpoint name.

        Returns:
            The endpoint instance.

        Raises:
            SMWValidationError: If the endpoint is not registered.
        """
        if name not in self._endpoints:
            raise SMWValidationError(f"Endpoint '{name}' is not registered")
        return self._endpoints[name]

    def make_request(
        self, action: str, params: dict[str, Any] | None = None, method: str = "GET"
    ) -> dict[str, Any]:
        """Make a request to the SMW API.

        Args:
            action: The API action/module name.
            params: Additional parameters for the request.
            method: HTTP method to use.

        Returns:
            The API response as a dictionary.

        Raises:
            SMWAPIError: If the API request fails.
        """
        # Prepare parameters
        request_params = {"action": action, "format": "json"}
        if params:
            request_params.update(params)

        try:
            if method.upper() == "GET":
                response = self.http_client.get(self.api_url, params=request_params)
            elif method.upper() == "POST":
                response = self.http_client.post(self.api_url, data=request_params)
            else:
                raise SMWValidationError(f"Unsupported HTTP method: {method}")

            # Check for API errors
            if "error" in response:
                error_info = response["error"]
                raise SMWAPIError(
                    f"API Error: {error_info.get('info', 'Unknown error')}",
                    response_data=error_info,
                )

            return response

        except SMWAPIError:
            # Re-raise SMW API errors as-is
            raise
        except Exception as e:
            # Wrap other exceptions
            raise SMWAPIError(f"Request failed: {e}") from e
