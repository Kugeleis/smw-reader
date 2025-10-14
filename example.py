#!/usr/bin/env python3
"""
Example usage of the SMW Reader API client.

This example demonstrates how to use the modular Semantic MediaWiki API client
to perform semantic queries using the 'ask' endpoint.
"""

from smw_reader import SMWClient
from smw_reader.endpoints.ask import AskEndpoint
from smw_reader.exceptions import SMWAPIError, SMWConnectionError


def demonstrate_client_usage(base_url: str):
    """Demonstrate basic client usage patterns."""
    print("=== SMW Reader Client Examples ===\n")

    # For this demo, we'll use a placeholder since live SMW instances may be unreliable
    # Replace with your actual SMW-enabled MediaWiki installation
    print("ℹ️  Note: This demo shows the API structure. Replace URL with your SMW instance.")
    client = SMWClient(base_url)  # Placeholder URL

    # Register the ask endpoint
    ask_endpoint = AskEndpoint(client)
    client.register_endpoint(ask_endpoint)

    # Return the ask_endpoint directly to maintain proper typing
    return client, ask_endpoint


def example_basic_query(client: SMWClient):
    """Example 1: Simple category query using the main client."""
    print("Example 1: Basic query using SMWClient.make_request()")
    print("-" * 55)

    result = client.make_request("ask", {"query": "[[Category:Person]]"})

    results_count = len(result.get("query", {}).get("results", {}))
    print(f"Found {results_count} pages in Category:Person")

    if results_count > 0:
        # Show first result as example
        results = result.get("query", {}).get("results", {})
        first_page = next(iter(results.keys()))
        print(f"First result: {first_page}")

    return result


def example_ask_endpoint(ask_endpoint, condition: str, printout: str):
    """Example 2: Using the Ask endpoint with properties."""
    print("\nExample 2: Query with properties using Ask endpoint")
    print("-" * 60)

    result = ask_endpoint.execute(query=f"[[{condition}]]|{printout}", limit=5)

    results_count = len(result.get("query", {}).get("results", {}))
    print(f"Found {results_count} {condition} with {printout} properties")
    return result


def example_convenience_method(ask_endpoint):
    """Example 3: Using the convenience ask method."""
    print("\nExample 3: Using convenience ask() method")
    print("-" * 50)

    # Use the ask convenience method
    result = ask_endpoint.ask("[[Category:Software]]", limit=3)

    results_count = len(result.get("query", {}).get("results", {}))
    print(f"Found {results_count} software pages")
    return result


def example_structured_query(ask_endpoint, conditions: list[str], printouts: list[str]):
    """Example 4: Structured query using query_pages method."""
    print("\nExample 4: Structured query using query_pages()")
    print("-" * 55)

    result = ask_endpoint.query_pages(
        conditions=build_conditions(conditions),
        printouts=build_printouts(printouts),
        limit=10,
        sort="Age",
        order="desc",
    )

    results_count = len(result.get("query", {}).get("results", {}))
    print(f"Found {results_count} featured software with license info")
    return result


def build_conditions(conditions: list[str]) -> list[str]:
    """Build conditions list for query_pages method."""
    return [f"[[{condition}]]" for condition in conditions]


def build_printouts(printouts: list[str]) -> list[str]:
    """Build printouts list for query_pages method."""
    return [f"?{printout}" for printout in printouts]


def main():
    """Main example function demonstrating SMW API usage with FSF Directory queries."""

    # Use FSF Directory as the primary example (correct API endpoint)
    base_url = "https://directory.fsf.org/w/"

    # FSF Directory-specific examples
    print("=== Free Software Directory (FSF) SMW Query Examples ===\n")

    # Example queries based on FSF Directory structure (verified working)
    fsf_queries = {
        "featured_software": {
            "condition": "Featured date::+",
            "printout": "?Name|?License|?Homepage URL|?Full description",
        },
        "gnu_software": {
            "condition": "Is GNU::Yes",
            "printout": "?Name|?License|?Interface|?Homepage URL",
        },
        "recent_software": {
            "condition": "Submitted date::+",
            "printout": "?Name|?License|?Submitted date|?Homepage URL",
        },
    }

    # Use working FSF Directory properties for structured example
    conditions = ["Featured date::+", "License::+"]
    printouts = ["Name", "License", "Homepage URL", "Featured date"]
    try:
        client, ask_endpoint = demonstrate_client_usage(base_url)

        # Run examples sequentially with FSF Directory queries
        example_basic_query(client)

        # Use FSF Directory-specific queries with utility functions
        featured_conditions = build_conditions([fsf_queries["featured_software"]["condition"]])
        featured_printouts = build_printouts(
            ["Name", "License", "Homepage URL", "Full description"]
        )
        featured_query = "|".join(featured_conditions + featured_printouts)

        print("\nExample 2: Featured Software Query (using utility functions)")
        print("-" * 62)
        featured_result = ask_endpoint.execute(query=featured_query, limit=5)
        featured_count = len(featured_result.get("query", {}).get("results", {}))
        print(f"Found {featured_count} featured software packages")

        print("\nExample: GNU Software Query (using utility functions)")
        print("-" * 60)
        gnu_conditions = build_conditions([fsf_queries["gnu_software"]["condition"]])
        gnu_printouts = build_printouts(["Name", "License", "Interface", "Homepage URL"])
        gnu_query = "|".join(gnu_conditions + gnu_printouts)

        gnu_result = ask_endpoint.execute(query=gnu_query, limit=5)
        gnu_count = len(gnu_result.get("query", {}).get("results", {}))
        print(f"Found {gnu_count} GNU software packages")

        example_convenience_method(ask_endpoint)
        example_structured_query(ask_endpoint, conditions, printouts)

        print("\n✅ All FSF Directory examples completed successfully!")

    except SMWConnectionError as e:
        print(f"❌ Connection error: {e}")
    except SMWAPIError as e:
        error_msg = str(e)
        if 'Unrecognized value for parameter "action": ask' in error_msg:
            print(f"❌ SMW Extension Missing: {e}")
            print("   This MediaWiki installation doesn't have Semantic MediaWiki extension!")
        else:
            print(f"❌ API error: {e}")

        if e.response_data:
            print(f"   Details: {e.response_data.get('info', 'No additional info')}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        # show_offline_examples()


if __name__ == "__main__":
    main()
