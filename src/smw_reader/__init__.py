"""SMW Reader - A modular Python client for Semantic MediaWiki API.

This package provides a clean, modular interface to the Semantic MediaWiki API
following best practices for maintainable and extensible code.

Example usage:
    from smw_reader import SMWClient, AskEndpoint

    # Create client
    client = SMWClient("https://example.com/wiki/")

    # Register and use Ask endpoint
    ask_endpoint = AskEndpoint(client)
    client.register_endpoint(ask_endpoint)

    # Execute a query
    results = ask_endpoint.ask("[[Category:Person]]|?Name|?Age")
"""

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

__version__ = "0.2.0"


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
