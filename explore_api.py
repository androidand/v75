"""
ATG API Explorer - Discover and test API endpoints
"""
import requests
import ssl
import json
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT:@SECLEVEL=1")
        kwargs["ssl_context"] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)


def test_endpoint(endpoint_name, url, description):
    """Test an API endpoint and return the results"""
    session = requests.Session()
    adapter = SSLAdapter()
    session.mount("https://", adapter)

    print(f"\n{'='*80}")
    print(f"Testing: {endpoint_name}")
    print(f"Description: {description}")
    print(f"URL: {url}")
    print(f"{'='*80}")

    try:
        response = session.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                # Save response to file for later analysis
                filename = f"api_responses/{endpoint_name.replace(' ', '_').replace('/', '_')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"✓ SUCCESS - Response saved to {filename}")

                # Print sample of the data structure
                if isinstance(data, dict):
                    print(f"Response keys: {list(data.keys())[:10]}")
                elif isinstance(data, list):
                    print(f"Response is a list with {len(data)} items")
                    if data:
                        print(f"First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")

                return {"success": True, "data": data}
            except json.JSONDecodeError:
                print(f"✗ ERROR - Response is not JSON")
                print(f"Content type: {response.headers.get('content-type')}")
                return {"success": False, "error": "Not JSON"}
        else:
            print(f"✗ FAILED - Status {response.status_code}")
            return {"success": False, "status_code": response.status_code}

    except requests.exceptions.Timeout:
        print(f"✗ TIMEOUT - Request took too long")
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        print(f"✗ ERROR - {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    """Explore various ATG API endpoints"""

    # Create directory for responses
    import os
    os.makedirs("api_responses", exist_ok=True)

    base_url = "https://www.atg.se/services/racinginfo/v1/api"

    # Get a recent Saturday for testing
    today = datetime.now()
    last_saturday = today - timedelta(days=(today.weekday() - 5) % 7)
    test_date = last_saturday.strftime("%Y-%m-%d")

    print(f"Using test date: {test_date}")

    # Endpoint configurations
    endpoints = [
        # Known working endpoints
        {
            "name": "calendar_day",
            "url": f"{base_url}/calendar/day/{test_date}",
            "description": "Get race calendar for a specific day"
        },

        # Potential calendar variations
        {
            "name": "calendar_week",
            "url": f"{base_url}/calendar/week/{test_date}",
            "description": "Get race calendar for a week"
        },
        {
            "name": "calendar_month",
            "url": f"{base_url}/calendar/month/{test_date[:7]}",  # YYYY-MM
            "description": "Get race calendar for a month"
        },

        # Track related endpoints
        {
            "name": "tracks",
            "url": f"{base_url}/tracks",
            "description": "Get list of all tracks"
        },
        {
            "name": "track_detail",
            "url": f"{base_url}/tracks/32",
            "description": "Get details for a specific track (Solvalla)"
        },

        # Results endpoints
        {
            "name": "results_day",
            "url": f"{base_url}/results/day/{test_date}",
            "description": "Get results for a specific day"
        },
        {
            "name": "results_game",
            "url": f"{base_url}/results/V75",
            "description": "Get V75 results"
        },

        # Statistics and odds
        {
            "name": "odds",
            "url": f"{base_url}/odds",
            "description": "Get current odds data"
        },
        {
            "name": "pools",
            "url": f"{base_url}/pools",
            "description": "Get betting pools data"
        },

        # Driver and trainer endpoints
        {
            "name": "drivers",
            "url": f"{base_url}/drivers",
            "description": "Get list of drivers"
        },
        {
            "name": "trainers",
            "url": f"{base_url}/trainers",
            "description": "Get list of trainers"
        },

        # Product/game types
        {
            "name": "products",
            "url": f"{base_url}/products",
            "description": "Get available betting products"
        },
        {
            "name": "games",
            "url": f"{base_url}/games",
            "description": "Get current games"
        },

        # Live/current data
        {
            "name": "live",
            "url": f"{base_url}/live",
            "description": "Get live racing data"
        },
        {
            "name": "live_races",
            "url": f"{base_url}/live/races",
            "description": "Get current live races"
        },
    ]

    results = []
    for endpoint in endpoints:
        result = test_endpoint(endpoint["name"], endpoint["url"], endpoint["description"])
        results.append({
            "name": endpoint["name"],
            "url": endpoint["url"],
            "success": result.get("success", False)
        })

    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"\n✓ Successful endpoints ({len(successful)}):")
    for r in successful:
        print(f"  - {r['name']}")

    print(f"\n✗ Failed endpoints ({len(failed)}):")
    for r in failed:
        print(f"  - {r['name']}")

    print(f"\nTotal tested: {len(results)}")
    print(f"Success rate: {len(successful)/len(results)*100:.1f}%")


if __name__ == "__main__":
    main()
