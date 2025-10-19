""".. include:: ../../README.md"""

from typing import Any

from .client import SMWClient
from .endpoints import AskEndpoint
from .exceptions import (
    SMWAPIError,
    SMWAuthenticationError,
    SMWConnectionError,
    SMWServerError,
    SMWValidationError,
)
from .http_client import RequestsHTTPClient
from .interfaces import APIEndpoint, HTTPClient

__all__ = [
    "SMWClient",
    "AskEndpoint",
    "SMWAPIError",
    "SMWConnectionError",
    "SMWAuthenticationError",
    "SMWValidationError",
    "SMWServerError",
    "APIEndpoint",
    "HTTPClient",
    "RequestsHTTPClient",
]

__version__ = "0.6.0"


def create_client(base_url: str, **kwargs: Any) -> SMWClient:
    """Create a configured SMW client with common endpoints.

    Args:
        base_url: Base URL of the MediaWiki installation.
        **kwargs: Additional arguments passed to SMWClient constructor.

    Returns:
        Configured SMWClient instance with Ask endpoint registered.
    """
    client = SMWClient(base_url, **kwargs)

    # Register common endpoints
    ask_endpoint = AskEndpoint(client)
    client.register_endpoint(ask_endpoint)

    return client


def main() -> None:
    """Main entry point for the CLI."""
    print("SMW Reader - Semantic MediaWiki API Client")
    print("Use 'create_client()' to get started with the API.")
