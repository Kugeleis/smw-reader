#!/usr/bin/env python3
"""
Minimal SMW Reader example using the core API.

This example demonstrates the cleanest way to use the SMW Reader API client
with the built-in utility methods for building semantic queries.
"""

from rich import print

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


def try_boxmatrix():
    """Test function to try boxmatrix."""
    print("Trying BoxMatrix (FRITZ!Box data)...")

    base_url = "https://boxmatrix.info/w"
    api_path = "api.php"

    try:
        client = SMWClient(base_url=base_url, api_path=api_path)
        ask_endpoint = AskEndpoint(client)
        conditions = ask_endpoint.build_conditions(["Category:FRITZ!Box-Family"])
        printouts = ask_endpoint.build_printouts(["WLAN1", "WLAN2", "RAM", "CPU-Clock"])

        result = ask_endpoint.query_pages(
            conditions=conditions,
            printouts=printouts,
            limit=5,
            sort="Name",
            order="asc",
        )

        # Display results
        results_data = result.get("query", {}).get("results", {})
        results_count = len(results_data)
        print(f"✅ Found {results_count} FRITZ!Box devices")

        # Show first few results and available properties
        for i, (name, data) in enumerate(list(results_data.items())[:3]):
            printouts = data.get("printouts", {})

            # Show what properties are actually available
            if i == 0:  # Only show for first item to avoid clutter
                print(f"   Available properties: {list(printouts.keys())}")

            # Extract values
            wlan1 = printouts.get("WLAN1", [])
            wlan2 = printouts.get("WLAN2", [])
            ram = printouts.get("RAM", [])
            cpu_clock = printouts.get("CPU-Clock", [])

            wlan1_val = wlan1[0] if wlan1 else "N/A"
            wlan2_val = wlan2[0] if wlan2 else "N/A"
            ram_val = ram[0] if ram else "N/A"
            cpu_val = cpu_clock[0] if cpu_clock else "N/A"

            display_name = name.split("#")[0]  # Remove fragment if present
            print(f"{i + 1}. {display_name}")
            print(f"   WLAN: {wlan1_val} (5GHz) / {wlan2_val} (2.4GHz)")
            print(f"   RAM: {ram_val}, CPU: {cpu_val}")

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


def main() -> None:
    """Main function demonstrating minimal structured SMW query."""
    minimal_query_example()
    try_boxmatrix()


if __name__ == "__main__":
    main()
