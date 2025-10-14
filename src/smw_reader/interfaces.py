"""Interfaces for the SMW API client following the open/closed principle."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import SMWClient


class APIEndpoint(ABC):
    """Abstract base class for SMW API endpoints.

    This interface allows for easy extension of new API endpoints
    while maintaining the open/closed principle.
    """

    def __init__(self, client: SMWClient) -> None:
        """Initialize the endpoint with a client instance.

        Args:
            client: The SMW client instance for making requests.
        """
        self._client = client

    @abstractmethod
    def execute(self, **params: Any) -> dict[str, Any]:
        """Execute the API endpoint with given parameters.

        Args:
            **params: Endpoint-specific parameters.

        Returns:
            The API response as a dictionary.

        Raises:
            SMWAPIError: If the API request fails.
        """
        pass

    @property
    @abstractmethod
    def endpoint_name(self) -> str:
        """The name of the API endpoint (e.g., 'ask', 'askargs', 'smwbrowse')."""
        pass


class HTTPClient(ABC):
    """Abstract interface for HTTP clients to enable dependency injection."""

    @abstractmethod
    def get(self, url: str, params: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """Make a GET request.

        Args:
            url: The URL to request.
            params: Query parameters.
            **kwargs: Additional request parameters.

        Returns:
            The response data.
        """
        pass

    @abstractmethod
    def post(self, url: str, data: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """Make a POST request.

        Args:
            url: The URL to request.
            data: Request body data.
            **kwargs: Additional request parameters.

        Returns:
            The response data.
        """
        pass
