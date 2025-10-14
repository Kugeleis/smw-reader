#!/usr/bin/env python3
"""
Minimal SMW Reader example using the core API.

This example demonstrates the cleanest way to use the SMW Reader API client
with the built-in utility methods for building semantic queries.
"""

from smw_reader import SMWClient
from smw_reader.endpoints.ask import AskEndpoint
from smw_reader.exceptions import SMWAPIError, SMWConnectionError


def minimal_query_example() -> None:
    """Demonstrate minimal query using core API with utility methods."""
    # Use FSF Directory as example endpoint
    base_url = "https://directory.fsf.org/w/"

    # Create client and endpoint
    client = SMWClient(base_url)
    ask_endpoint = AskEndpoint(client)
    client.register_endpoint(ask_endpoint)

    print("=== Minimal SMW Query Example ===")
    print("Querying FSF Directory for GNU software...\n")

    try:
        # Use the built-in utility methods to build query components
        conditions = AskEndpoint.build_conditions(["Is GNU::Yes"])
        printouts = AskEndpoint.build_printouts(["Name", "License"])

        # Execute query using the structured query_pages method
        result = ask_endpoint.query_pages(
            conditions=conditions,
            printouts=printouts,
            limit=5,
            sort="Name",
            order="asc",
        )

        # Display results
        results_count = len(result.get("query", {}).get("results", {}))
        print(f"✅ Found {results_count} GNU software packages")

        # Show first few results
        results = result.get("query", {}).get("results", {})
        for i, (name, _) in enumerate(list(results.items())[:3]):
            print(f"{i + 1}. {name}")

    except SMWConnectionError as e:
        print(f"❌ Connection error: {e}")
        return None
    except SMWAPIError as e:
        print(f"❌ API error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def main() -> None:
    """Main function demonstrating minimal structured SMW query."""
    minimal_query_example()


if __name__ == "__main__":
    main()
