"""HTTP client implementation for SMW API requests."""

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

from .exceptions import SMWConnectionError, SMWServerError
from .interfaces import HTTPClient


class RequestsHTTPClient(HTTPClient):
    """HTTP client implementation using urllib (no external dependencies).

    This implementation uses only standard library modules to avoid
    external dependencies while providing robust HTTP functionality.
    """

    def __init__(self, timeout: float = 30.0, user_agent: str = "SMW-Reader/0.1.0") -> None:
        """Initialize the HTTP client.

        Args:
            timeout: Request timeout in seconds.
            user_agent: User agent string for requests.
        """
        self.timeout = timeout
        self.user_agent = user_agent

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        """Make a GET request.

        Args:
            url: The URL to request.
            params: Query parameters.
            **kwargs: Additional request parameters.

        Returns:
            The response data as a dictionary.

        Raises:
            SMWConnectionError: If the connection fails.
            SMWServerError: If the server returns an error.
        """
        if params:
            # Convert parameters to strings and encode
            str_params = {k: str(v) for k, v in params.items()}
            query_string = urllib.parse.urlencode(str_params)
            url = f"{url}?{query_string}"

        return self._make_request(url, method="GET", **kwargs)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        """Make a POST request.

        Args:
            url: The URL to request.
            data: Request body data.
            **kwargs: Additional request parameters.

        Returns:
            The response data as a dictionary.

        Raises:
            SMWConnectionError: If the connection fails.
            SMWServerError: If the server returns an error.
        """
        return self._make_request(url, method="POST", data=data, **kwargs)

    def _make_request(
        self, url: str, method: str = "GET", data: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make an HTTP request.

        Args:
            url: The URL to request.
            method: HTTP method.
            data: Request body data for POST requests.
            **kwargs: Additional request parameters.

        Returns:
            The response data as a dictionary.

        Raises:
            SMWConnectionError: If the connection fails.
            SMWServerError: If the server returns an error.
        """
        try:
            # Prepare request
            req_data = None
            if data and method == "POST":
                req_data = urllib.parse.urlencode(data).encode("utf-8")

            request = urllib.request.Request(url, data=req_data, method=method)
            request.add_header("User-Agent", self.user_agent)
            request.add_header("Accept", "application/json")

            if req_data:
                request.add_header("Content-Type", "application/x-www-form-urlencoded")

            # Make request
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response_text = response.read().decode("utf-8")

                # Try to parse JSON response
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError as e:
                    raise SMWServerError(f"Invalid JSON response: {e}") from e

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else "No error details"
            raise SMWServerError(
                f"HTTP {e.code}: {e.reason}. Response: {error_body}",
                status_code=e.code,
                response_data={"error": error_body},
            ) from e
        except urllib.error.URLError as e:
            raise SMWConnectionError(f"Connection error: {e.reason}") from e
        except Exception as e:
            raise SMWConnectionError(f"Unexpected error: {e}") from e
