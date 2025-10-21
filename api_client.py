"""
ATG API Client - Type-safe client for ATG Racing Information API
"""

import requests
import ssl
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta

from models import (
    RaceDay, Game, Horse, Race,
    parse_race_day, parse_game, parse_horse
)


class SSLAdapter(HTTPAdapter):
    """Custom SSL adapter for ATG API compatibility"""

    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT:@SECLEVEL=1")
        kwargs["ssl_context"] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)


class ATGAPIClient:
    """
    Client for ATG Racing Information API v1

    Base URL: https://www.atg.se/services/racinginfo/v1/api
    """

    BASE_URL = "https://www.atg.se/services/racinginfo/v1/api"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 10):
        """
        Initialize API client

        Args:
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create requests session with proper configuration"""
        session = requests.Session()

        # Add SSL adapter
        adapter = SSLAdapter()
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.atg.se/',
        })

        # Add API key if provided
        if self.api_key:
            session.headers['Authorization'] = f'Bearer {self.api_key}'

        return session

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Make GET request to API

        Args:
            endpoint: API endpoint path
            params: Optional query parameters

        Returns:
            JSON response as dict, or None on error
        """
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(f"Access denied to {url}")
                print("This may require:")
                print("- API key/authentication")
                print("- Swedish IP address")
                print("- Different access method")
                return None
            else:
                print(f"Error: HTTP {response.status_code} for {url}")
                return None

        except requests.exceptions.Timeout:
            print(f"Timeout accessing {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    # Calendar endpoints

    def get_calendar_day(self, date: str) -> Optional[RaceDay]:
        """
        Get race calendar for a specific day

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            RaceDay object or None

        Example:
            >>> client = ATGAPIClient()
            >>> race_day = client.get_calendar_day("2025-10-25")
        """
        data = self._get(f"calendar/day/{date}")
        if data:
            return parse_race_day(data)
        return None

    def get_calendar_week(self, date: str) -> Optional[Dict]:
        """
        Get race calendar for a week

        Args:
            date: Any date in the week (YYYY-MM-DD)

        Returns:
            Week calendar data or None
        """
        return self._get(f"calendar/week/{date}")

    def get_calendar_month(self, year_month: str) -> Optional[Dict]:
        """
        Get race calendar for a month

        Args:
            year_month: Year and month in YYYY-MM format

        Returns:
            Month calendar data or None
        """
        return self._get(f"calendar/month/{year_month}")

    # Game endpoints

    def get_game(self, game_id: str) -> Optional[Game]:
        """
        Get detailed game data

        Args:
            game_id: Game ID (e.g., "V75_2025-10-25_32_5")

        Returns:
            Game object with all races or None

        Example:
            >>> client = ATGAPIClient()
            >>> game = client.get_game("V75_2025-10-25_32_5")
            >>> for race in game.races:
            ...     print(f"Race {race.number}: {race.name}")
        """
        data = self._get(f"games/{game_id}")
        if data:
            return parse_game(data)
        return None

    # Horse endpoints

    def get_horse(self, horse_id: int) -> Optional[Horse]:
        """
        Get detailed horse information

        Args:
            horse_id: Horse ID

        Returns:
            Horse object or None

        Example:
            >>> client = ATGAPIClient()
            >>> horse = client.get_horse(789012)
            >>> print(f"{horse.name} ({horse.get_nationality()})")
        """
        data = self._get(f"horses/{horse_id}")
        if data:
            return parse_horse(data)
        return None

    # Race endpoints

    def get_race(self, race_id: str) -> Optional[Race]:
        """
        Get detailed race information

        Args:
            race_id: Race ID (format: YYYY-MM-DD_track-id_race-number)

        Returns:
            Race object or None
        """
        data = self._get(f"races/{race_id}")
        if data:
            from models import parse_race
            return parse_race(data)
        return None

    def get_race_start(self, race_id: str) -> Optional[Dict]:
        """Get race start information"""
        return self._get(f"races/{race_id}/start")

    def get_race_result(self, race_id: str) -> Optional[Dict]:
        """Get race result"""
        return self._get(f"races/{race_id}/result")

    def get_race_pools(self, race_id: str) -> Optional[Dict]:
        """Get betting pools for a race"""
        return self._get(f"races/{race_id}/pools")

    # Track endpoints

    def get_tracks(self) -> Optional[Dict]:
        """Get list of all tracks"""
        return self._get("tracks")

    def get_track(self, track_id: int) -> Optional[Dict]:
        """Get track details"""
        return self._get(f"tracks/{track_id}")

    def get_track_program(self, track_id: int, date: str) -> Optional[Dict]:
        """Get track program for a date"""
        return self._get(f"tracks/{track_id}/program/{date}")

    # Results endpoints

    def get_results_day(self, date: str) -> Optional[Dict]:
        """Get results for a specific day"""
        return self._get(f"results/day/{date}")

    def get_results_game_type(self, game_type: str) -> Optional[Dict]:
        """Get results for a game type (e.g., V75)"""
        return self._get(f"results/{game_type}")

    # Convenience methods

    def get_next_saturday(self) -> str:
        """Get next Saturday's date"""
        today = datetime.now()
        days_ahead = (5 - today.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        next_saturday = today + timedelta(days=days_ahead)
        return next_saturday.strftime("%Y-%m-%d")

    def get_next_v75(self) -> Optional[RaceDay]:
        """
        Get next V75 race day

        Returns:
            RaceDay object for next Saturday or None

        Example:
            >>> client = ATGAPIClient()
            >>> race_day = client.get_next_v75()
            >>> v75_games = race_day.get_v75_games()
        """
        next_saturday = self.get_next_saturday()
        return self.get_calendar_day(next_saturday)

    def get_v75_game_for_date(self, date: str) -> Optional[Game]:
        """
        Get V75 game data for a specific date

        Args:
            date: Date in YYYY-MM-DD format

        Returns:
            Complete Game object with all races or None

        Example:
            >>> client = ATGAPIClient()
            >>> game = client.get_v75_game_for_date("2025-10-25")
            >>> if game:
            ...     for race in game.races:
            ...         print(f"Race {race.number} has {len(race.starts)} horses")
        """
        race_day = self.get_calendar_day(date)
        if not race_day:
            return None

        v75_games = race_day.get_v75_games()
        if not v75_games:
            return None

        game_id = v75_games[0].id
        return self.get_game(game_id)


# Convenience function for quick access
def get_next_v75_game() -> Optional[Game]:
    """
    Quick function to get next V75 game

    Returns:
        Game object with all races or None

    Example:
        >>> from api_client import get_next_v75_game
        >>> game = get_next_v75_game()
        >>> if game:
        ...     print(f"V75 Game: {game.id}")
    """
    client = ATGAPIClient()
    next_saturday = client.get_next_saturday()
    return client.get_v75_game_for_date(next_saturday)


if __name__ == "__main__":
    """Test API client"""
    print("ATG API Client Test")
    print("=" * 80)

    client = ATGAPIClient()

    # Test 1: Get next Saturday
    next_saturday = client.get_next_saturday()
    print(f"\nNext Saturday: {next_saturday}")

    # Test 2: Get calendar for next Saturday
    print(f"\nFetching calendar for {next_saturday}...")
    race_day = client.get_calendar_day(next_saturday)

    if race_day:
        print(f"✓ Success!")
        print(f"  Date: {race_day.date}")
        print(f"  Tracks: {len(race_day.tracks)}")

        v75_track = race_day.get_v75_track()
        if v75_track:
            print(f"  V75 Track: {v75_track.name} (ID: {v75_track.id})")

        v75_games = race_day.get_v75_games()
        if v75_games:
            print(f"  V75 Games: {len(v75_games)}")
            for game in v75_games:
                print(f"    - {game.id}: {len(game.races)} races")
    else:
        print("✗ Failed to fetch calendar")

    # Test 3: Try to get game data
    if race_day:
        v75_games = race_day.get_v75_games()
        if v75_games:
            game_id = v75_games[0].id
            print(f"\nFetching game data: {game_id}...")
            game = client.get_game(game_id)

            if game:
                print(f"✓ Success!")
                print(f"  Game ID: {game.id}")
                print(f"  Status: {game.status}")
                print(f"  Races: {len(game.races)}")

                for race in game.races[:2]:  # Show first 2 races
                    print(f"\n  Race {race.number}: {race.name}")
                    print(f"    Distance: {race.distance}m")
                    print(f"    Start: {race.start_method}")
                    print(f"    Horses: {len(race.starts)}")

                    for start in race.starts[:3]:  # Show first 3 horses
                        if start.horse:
                            print(f"      {start.number}. {start.horse.name} "
                                  f"({start.horse.get_nationality()})")
            else:
                print("✗ Failed to fetch game data")

    print("\n" + "=" * 80)
    print("Test complete")
