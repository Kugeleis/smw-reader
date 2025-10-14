#!/usr/bin/env python3
"""
FSF Directory query examples.

This module contains example functions for querying the Free Software Foundation
Directory using the SMW Reader API client. These are usage examples, not core library code.
"""

from smw_reader import SMWClient
from smw_reader.endpoints.ask import AskEndpoint
from smw_reader.exceptions import SMWAPIError, SMWConnectionError


def query_fsf_directory() -> dict | None:
    """Query the FSF Directory for featured software with licenses.

    This is an example function demonstrating how to query a real SMW instance.

    Returns:
        Query result dictionary or None if error occurred

    Example:
        >>> result = query_fsf_directory()
        >>> if result:
        ...     count = len(result.get("query", {}).get("results", {}))
        ...     print(f"Found {count} software packages")
    """
    # FSF Directory API endpoint
    base_url = "https://directory.fsf.org/w/"

    # Create client and register ask endpoint
    client = SMWClient(base_url)
    ask_endpoint = AskEndpoint(client)
    client.register_endpoint(ask_endpoint)

    # Define query parameters using FSF Directory properties
    conditions = ["Featured date::+", "License::+"]
    printouts = ["Name", "License", "Homepage URL", "Featured date"]

    print("=== Querying FSF Directory for Featured Software with Licenses ===")

    try:
        # Execute structured query using utility functions built into AskEndpoint
        result = ask_endpoint.query_pages(
            conditions=AskEndpoint.build_conditions(conditions),
            printouts=AskEndpoint.build_printouts(printouts),
            limit=10,
            sort="Featured date",
            order="desc",
        )

        # Process results
        results_count = len(result.get("query", {}).get("results", {}))
        print(f"Found {results_count} featured software packages with license info")

        # Display first few results
        results = result.get("query", {}).get("results", {})
        for i, (name, data) in enumerate(list(results.items())[:3]):
            print(f"\n{i + 1}. {name}")
            printouts_data = data.get("printouts", {})

            license_info = printouts_data.get("License", [])
            homepage = printouts_data.get("Homepage URL", [])
            featured_date = printouts_data.get("Featured date", [])

            # Extract clean values from SMW data structures
            license_display = "Unknown"
            if license_info and isinstance(license_info[0], dict):
                license_display = license_info[0].get("fulltext", "Unknown").replace("License:", "")
            elif license_info:
                license_display = str(license_info[0])

            homepage_display = homepage[0] if homepage else "No URL"

            featured_display = "Unknown"
            if featured_date and isinstance(featured_date[0], dict):
                featured_display = featured_date[0].get("raw", "Unknown")
            elif featured_date:
                featured_display = str(featured_date[0])

            print(f"   License: {license_display}")
            print(f"   Homepage: {homepage_display}")
            print(f"   Featured: {featured_display}")

        return result

    except SMWConnectionError as e:
        print(f"❌ Connection error: {e}")
        return None
    except SMWAPIError as e:
        print(f"❌ API error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def query_fsf_gnu_software() -> dict | None:
    """Query the FSF Directory for GNU software packages.

    This is an example function demonstrating a different type of query
    against the same SMW instance.

    Returns:
        Query result dictionary or None if error occurred
    """
    base_url = "https://directory.fsf.org/w/"

    client = SMWClient(base_url)
    ask_endpoint = AskEndpoint(client)
    client.register_endpoint(ask_endpoint)

    conditions = ["Is GNU::Yes"]
    printouts = ["Name", "License", "Interface", "Homepage URL"]

    try:
        result = ask_endpoint.query_pages(
            conditions=AskEndpoint.build_conditions(conditions),
            printouts=AskEndpoint.build_printouts(printouts),
            limit=20,
            sort="Name",
            order="asc",
        )

        results_count = len(result.get("query", {}).get("results", {}))
        print(f"Found {results_count} GNU software packages")

        return result

    except (SMWConnectionError, SMWAPIError, Exception) as e:
        print(f"❌ Error querying GNU software: {e}")
        return None


def main() -> None:
    """Main function demonstrating FSF Directory queries."""
    print("=== FSF Directory SMW Query Examples ===\n")

    # Example 1: Query FSF Directory for featured software
    print("1. Featured Software Query:")
    query_fsf_directory()

    print("\n" + "=" * 60 + "\n")

    # Example 2: Query FSF Directory for GNU software
    print("2. GNU Software Query:")
    query_fsf_gnu_software()


if __name__ == "__main__":
    main()
