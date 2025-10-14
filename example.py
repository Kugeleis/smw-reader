#!/usr/bin/env python3
"""
Example usage of the SMW Reader API client.

This example demonstrates how to use the modular Semantic MediaWiki API client
to perform semantic queries using the 'ask' endpoint.
"""

from smw_reader import SMWClient
from smw_reader.endpoints.ask import AskEndpoint
from smw_reader.exceptions import SMWAPIError, SMWConnectionError


def demonstrate_client_usage():
    """Demonstrate basic client usage patterns."""
    print("=== SMW Reader Client Examples ===\n")
    
    # For this demo, we'll use a placeholder since live SMW instances may be unreliable
    # Replace with your actual SMW-enabled MediaWiki installation
    print("ℹ️  Note: This demo shows the API structure. Replace URL with your SMW instance.")
    client = SMWClient("https://directory.fsf.org/w")  # Placeholder URL

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
    print(f"Found {results_count} people over 25 with occupation info")
    return result

def build_conditions(conditions: list[str])->list[str]:
    """ Build conditions list for query_pages method. """
    return [f"[[{condition}]]" for condition in conditions]

def build_printouts(printouts: list[str])->list[str]:
    """ Build printouts list for query_pages method. """
    return [f"?{printout}" for printout in printouts]

def show_offline_examples():
    """Show example usage patterns when offline/connection fails."""
    print("\n" + "="*70)
    print("SMW API UNAVAILABLE - Showing usage examples and requirements")
    print("="*70)

    print("\n📚 Basic Usage Pattern:")
    print("```python")
    print("from smw_reader import SMWClient")
    print("from smw_reader.endpoints.ask import AskEndpoint")
    print()
    print("# Create client")
    print('client = SMWClient("https://your-wiki.org/w/")')
    print()
    print("# Register ask endpoint")
    print("ask_endpoint = AskEndpoint(client)")
    print("client.register_endpoint(ask_endpoint)")
    print()
    print("# Execute queries")
    print('result = ask_endpoint.ask("[[Category:Person]]")')
    print("```")

    print("\n🔍 Query Examples:")
    print("• Simple category: [[Category:Person]]")
    print("• With properties: [[Category:Person]]|?Name|?Age")
    print("• With conditions: [[Category:Person]][[Age::>25]]")
    print("• Complex query: [[Category:Software]][[License::Free]]|?Version|?Developer|sort=Name")

    print("\n⚙️ Method Options:")
    print("• ask_endpoint.execute(query='...', limit=10)")
    print("• ask_endpoint.ask('...', limit=5, sort='Name')")
    print("• ask_endpoint.query_pages(conditions=['[[Category:X]]'], printouts=['?Name'])")

    print("\n� Expected Response Structure:")
    print("```json")
    print("{")
    print('  "query": {')
    print('    "results": {')
    print('      "John Doe": {')
    print('        "printouts": {')
    print('          "Name": ["John Doe"],')
    print('          "Age": [30]')
    print("        },")
    print('        "fulltext": "John Doe",')
    print('        "fullurl": "https://wiki.example.org/John_Doe"')
    print("      }")
    print("    }")
    print("  }")
    print("}")
    print("```")

    print("\n�💡 Requirements for SMW API:")
    print("   • MediaWiki with Semantic MediaWiki extension installed")
    print("   • API endpoint that supports 'ask' action")
    print("   • Example SMW instances:")
    print("     - https://www.semantic-mediawiki.org/w/ (official)")
    print("     - Your own MediaWiki + SMW installation")
    print()
    print("❌ Note: Regular MediaWiki (like Wikipedia) does NOT support SMW queries")
    print("   The 'ask' action is only available with SMW extension")


def main():
    """Main example function demonstrating SMW API usage."""

    condition = "Category:Email-software"
    printout = "?Name|?Age"

    conditions = ["Category:Person", "Age::>25"]
    printouts = ["Name", "Age", "Occupation"]
    try:
        client, ask_endpoint = demonstrate_client_usage()

        # Run examples sequentially
        example_basic_query(client)
        example_ask_endpoint(ask_endpoint, condition, printout)
        example_convenience_method(ask_endpoint)
        example_structured_query(ask_endpoint, conditions, printouts)

        print("\n✅ All examples completed successfully!")

    except SMWConnectionError as e:
        print(f"❌ Connection error: {e}")
        show_offline_examples()
    except SMWAPIError as e:
        error_msg = str(e)
        if "Unrecognized value for parameter \"action\": ask" in error_msg:
            print(f"❌ SMW Extension Missing: {e}")
            print("   This MediaWiki installation doesn't have Semantic MediaWiki extension!")
        else:
            print(f"❌ API error: {e}")
        
        if e.response_data:
            print(f"   Details: {e.response_data.get('info', 'No additional info')}")
        show_offline_examples()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        show_offline_examples()


if __name__ == "__main__":
    main()
