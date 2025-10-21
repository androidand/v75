"""
ATG API Explorer - Discover and test API endpoints with proper headers
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

    # Add browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.atg.se/',
        'Origin': 'https://www.atg.se',
    }

    print(f"\n{'='*80}")
    print(f"Testing: {endpoint_name}")
    print(f"Description: {description}")
    print(f"URL: {url}")
    print(f"{'='*80}")

    try:
        response = session.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                # Save response to file for later analysis
                import os
                os.makedirs("api_responses", exist_ok=True)
                filename = f"api_responses/{endpoint_name.replace(' ', '_').replace('/', '_')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"✓ SUCCESS - Response saved to {filename}")

                # Print sample of the data structure
                if isinstance(data, dict):
                    print(f"Response keys: {list(data.keys())[:15]}")
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

    base_url = "https://www.atg.se/services/racinginfo/v1/api"

    # Use a past date that should have data (last Saturday)
    # Today is 2025-10-21, so last Saturday was 2025-10-18
    test_date = "2024-10-05"  # Use a date from commit history
    print(f"Using test date: {test_date}")

    # First, test the known working endpoint
    print("\n" + "="*80)
    print("TESTING KNOWN WORKING ENDPOINTS FIRST")
    print("="*80)

    # Get game ID from calendar first
    calendar_result = test_endpoint(
        "calendar_day",
        f"{base_url}/calendar/day/{test_date}",
        "Get race calendar for a specific day"
    )

    game_id = None
    if calendar_result.get("success"):
        data = calendar_result["data"]
        games = data.get("games", {})
        v75_games = games.get("V75", [])
        if v75_games:
            game_id = v75_games[0].get("id")
            print(f"\nFound V75 game ID: {game_id}")

    # Additional endpoints to test
    endpoints = []

    if game_id:
        endpoints.append({
            "name": "game_detail",
            "url": f"{base_url}/games/{game_id}",
            "description": "Get detailed game data"
        })

        # Extract race IDs and track IDs from calendar
        if calendar_result.get("success"):
            data = calendar_result["data"]
            tracks = data.get("tracks", [])
            if tracks:
                track_id = tracks[0].get("id")
                if track_id:
                    endpoints.append({
                        "name": "track_program",
                        "url": f"{base_url}/tracks/{track_id}/program/{test_date}",
                        "description": "Get track program for a date"
                    })

            # Get race IDs
            v75_games = data.get("games", {}).get("V75", [])
            if v75_games and v75_games[0].get("races"):
                race_id = v75_games[0]["races"][0]
                endpoints.append({
                    "name": "race_detail",
                    "url": f"{base_url}/races/{race_id}",
                    "description": "Get detailed race information"
                })
                endpoints.append({
                    "name": "race_start",
                    "url": f"{base_url}/races/{race_id}/start",
                    "description": "Get race start information"
                })
                endpoints.append({
                    "name": "race_pools",
                    "url": f"{base_url}/races/{race_id}/pools",
                    "description": "Get race betting pools"
                })
                endpoints.append({
                    "name": "race_result",
                    "url": f"{base_url}/races/{race_id}/result",
                    "description": "Get race result"
                })

    # More endpoints to explore
    endpoints.extend([
        {
            "name": "calendar_week",
            "url": f"{base_url}/calendar/week/{test_date}",
            "description": "Get race calendar for a week"
        },
        {
            "name": "products",
            "url": f"{base_url}/products",
            "description": "Get available betting products"
        },
        {
            "name": "game_types",
            "url": f"{base_url}/gametypes",
            "description": "Get available game types"
        },
        {
            "name": "tracks_list",
            "url": f"{base_url}/tracks",
            "description": "Get list of all tracks"
        },
    ])

    results = [{"name": "calendar_day", "url": calendar_result, "success": calendar_result.get("success", False)}]

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
