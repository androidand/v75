import requests
import ssl
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT:@SECLEVEL=1")  # Lower security level
        kwargs["ssl_context"] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)


def fetch_race_day_data(date):
    url = f"https://www.atg.se/services/racinginfo/v1/api/calendar/day/{date}"
    session = requests.Session()
    adapter = SSLAdapter()
    session.mount("https://", adapter)
    print(f"Fetching race day data for {date} from URL: {url}")
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(
            f"Error: Unable to fetch data from {url}. Status Code: {response.status_code}"
        )
        return None


def fetch_v75_game_data(game_id):
    url = f"https://www.atg.se/services/racinginfo/v1/api/games/{game_id}"
    session = requests.Session()
    adapter = SSLAdapter()
    session.mount("https://", adapter)

    print(f"Fetching game data from URL: {url}")
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Error: Unable to fetch data from {url}. Status Code: {response.status_code}"
        )
        return None


def fetch_horse_data(horse_id):
    """Fetches detailed horse data including pedigree from the API."""
    url = f"https://www.atg.se/services/racinginfo/v1/api/horses/{horse_id}"
    session = requests.Session()
    adapter = SSLAdapter()
    session.mount("https://", adapter)
    response = session.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching horse data for ID {horse_id}: {response.status_code}")
        return None


def get_horse_nationality_from_game(horse):
    """Fetches the horse nationality from the game data, checking the pedigree."""
    pedigree = horse.get("pedigree", {})
    father = pedigree.get("father", {})
    mother = pedigree.get("mother", {})
    grandfather = pedigree.get("grandfather", {})

    if father.get("nationality"):
        return father["nationality"]
    elif mother.get("nationality"):
        return mother["nationality"]
    elif grandfather.get("nationality"):
        return grandfather["nationality"]
    return None


def get_horse_nationality(horse, detailed_horse_data=None):
    """Attempts to find the horse's nationality, checking first in the game data, then the API."""
    horse_nationality = horse.get("nationality")

    if horse_nationality:
        return horse_nationality
    elif detailed_horse_data:
        # Fallback to pedigree data from the detailed horse data if nationality is not found
        return get_horse_nationality_from_game(detailed_horse_data) or "Unknown"

    return "Unknown"


def display_races_and_horses(races):
    """Displays race and horse data, checking for nationality in the game object first."""
    sorted_races = sorted(races, key=lambda race: race["scheduledStartTime"])

    for idx, race in enumerate(sorted_races, start=1):
        race_id = race.get("id", "N/A")
        race_number = race.get("number", idx)
        race_name = race.get("name", "N/A")
        start_time = race.get("startTime", "N/A")
        scheduled_start_time = race.get("scheduledStartTime", "N/A")
        distance = race.get("distance", "N/A")
        start_method = race.get("startMethod", "N/A")

        print(f"\nAvdelning {idx} (Race {race_number}, ID: {race_id})")
        print(f"Name: {race_name}")
        print(f"Start Time: {start_time} (Scheduled: {scheduled_start_time})")
        print(f"Distance: {distance} meters, Start Method: {start_method}")

        print("Horses:")
        for start in race.get("starts", []):
            horse = start["horse"]
            driver = start.get("driver", {})
            horse_name = horse.get("name", "Unknown")
            horse_id = horse.get("id")

            # First, try to get nationality from the game data (pedigree)
            horse_nationality = get_horse_nationality_from_game(horse)

            # If not found in game data, then fallback to detailed API lookup
            if horse_nationality is None:
                detailed_horse_data = fetch_horse_data(horse_id)
                horse_nationality = get_horse_nationality(horse, detailed_horse_data)

            driver_first_name = driver.get("firstName", "Unknown")
            driver_last_name = driver.get("lastName", "Unknown")
            trainer_last_name = driver.get("lastName", "Unknown")
            earnings = horse.get("money", "N/A")

            print(
                f"{start['number']}. {horse_name} ({horse_nationality}) - Trainer: {trainer_last_name}, Driver: {driver_first_name} {driver_last_name}, Earnings: {earnings} SEK"
            )


def get_next_saturday():
    today = datetime.now()
    next_saturday = today + timedelta((5 - today.weekday()) % 7)  # Saturday is day 5
    return next_saturday.strftime("%Y-%m-%d")


def list_v75_dates_for_year():
    """Lists all Saturdays (V75 race days) for the current year."""
    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year, 12, 31)
    saturdays = []

    while start_date <= end_date:
        if start_date.weekday() == 5:  # If it's a Saturday
            saturdays.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)

    print("V75 Dates for the current year:")
    for date in saturdays:
        print(f"- {date}")


def main(input_date=None):
    if input_date == "list-dates":
        list_v75_dates_for_year()
    else:
        if not input_date:
            input_date = get_next_saturday()
        print(f"Next Game Day: {input_date}")

        race_day_data = fetch_race_day_data(input_date)
        if race_day_data:
            tracks = race_day_data.get("tracks", [])
            for track in tracks:
                if track.get("biggestGameType") == "V75":
                    track_id = track["id"]
                    print(f"V75 track found: {track['name']} (ID: {track_id})")

                    # Accessing games.V75 and extracting the first game's ID and races
                    games_info = race_day_data.get("games", {})
                    v75_games = games_info.get("V75", [])
                    if v75_games:
                        game_id = v75_games[0].get("id")  # Fetch the game ID from V75[0]
                        race_ids = v75_games[0].get("races", [])

                        print(f"V75 Game ID: {game_id}")
                        print(f"Race IDs: {', '.join(race_ids)}")

                        # Fetch game data using the game ID
                        game_data = fetch_v75_game_data(game_id)
                        if game_data:
                            display_races_and_horses(game_data.get("races", []))
                        else:
                            print(f"Failed to fetch game data for {game_id}")
                    else:
                        print(
                            f"No V75 game data found for {input_date} at {track['name']} (ID: {track_id})."
                        )
                    break
            else:
                print(f"No V75 track found for {input_date}")
        else:
            print(f"No race data available for {input_date}")


# Usage example:
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
