"""
Usage Examples for ATG API Client and Models

This file demonstrates how to use the type-safe API client and dataclass models.
"""

from api_client import ATGAPIClient, get_next_v75_game
from models import Race, Horse, RaceStart, Game


def example_1_get_next_v75():
    """
    Example 1: Get next V75 race day and display basic information
    """
    print("Example 1: Get Next V75")
    print("=" * 80)

    client = ATGAPIClient()

    # Get next Saturday's date
    next_saturday = client.get_next_saturday()
    print(f"Next Saturday: {next_saturday}")

    # Get race day calendar
    race_day = client.get_calendar_day(next_saturday)

    if not race_day:
        print("Could not fetch race day data (API may be restricted)")
        return

    print(f"\nDate: {race_day.date}")
    print(f"Number of tracks: {len(race_day.tracks)}")

    # Find V75 track
    v75_track = race_day.get_v75_track()
    if v75_track:
        print(f"\nV75 Track: {v75_track.name} (ID: {v75_track.id})")

    # Get V75 games
    v75_games = race_day.get_v75_games()
    if v75_games:
        print(f"V75 Games: {len(v75_games)}")
        for game_info in v75_games:
            print(f"  - {game_info.id}")
            print(f"    Races: {len(game_info.races)}")


def example_2_analyze_game():
    """
    Example 2: Get game data and analyze races
    """
    print("\nExample 2: Analyze V75 Game")
    print("=" * 80)

    client = ATGAPIClient()
    next_saturday = client.get_next_saturday()

    # Get complete game data
    game = client.get_v75_game_for_date(next_saturday)

    if not game:
        print("Could not fetch game data")
        return

    print(f"Game ID: {game.id}")
    print(f"Status: {game.status.value}")
    print(f"Number of races: {len(game.races)}")

    # Analyze each race
    for race in game.races:
        print(f"\n{'=' * 60}")
        print(f"Race {race.number}: {race.name}")
        print(f"{'=' * 60}")
        print(f"Distance: {race.distance}m")
        print(f"Start method: {race.start_method.value if race.start_method else 'Unknown'}")
        print(f"Scheduled start: {race.scheduled_start_time}")
        print(f"Number of horses: {len(race.starts)}")

        # Show horses
        print(f"\nStarters:")
        for start in race.starts:
            if start.horse:
                print(f"  {start.number}. {start.horse.name} "
                      f"({start.horse.get_nationality()}) - "
                      f"{start.horse.money:,} SEK")
                if start.driver:
                    print(f"      Driver: {start.driver.full_name}")
                if start.trainer:
                    print(f"      Trainer: {start.trainer.full_name}")


def example_3_horse_details():
    """
    Example 3: Get detailed horse information
    """
    print("\nExample 3: Horse Details")
    print("=" * 80)

    client = ATGAPIClient()

    # This would work if we had a specific horse ID
    # For demo purposes, let's show how it would be used
    horse_id = 789012  # Example ID

    horse = client.get_horse(horse_id)

    if not horse:
        print(f"Could not fetch horse {horse_id}")
        return

    print(f"Name: {horse.name}")
    print(f"ID: {horse.id}")
    print(f"Nationality: {horse.get_nationality()}")
    print(f"Age: {horse.age}")
    print(f"Sex: {horse.sex.value if horse.sex else 'Unknown'}")
    print(f"Career Earnings: {horse.money:,} SEK")

    if horse.pedigree:
        print(f"\nPedigree:")
        if horse.pedigree.father:
            print(f"  Father: {horse.pedigree.father.name} "
                  f"({horse.pedigree.father.nationality})")
        if horse.pedigree.mother:
            print(f"  Mother: {horse.pedigree.mother.name} "
                  f"({horse.pedigree.mother.nationality})")
        if horse.pedigree.grandfather:
            print(f"  Grandfather: {horse.pedigree.grandfather.name} "
                  f"({horse.pedigree.grandfather.nationality})")


def example_4_find_top_earners():
    """
    Example 4: Find top earning horses in a race
    """
    print("\nExample 4: Find Top Earners in Race")
    print("=" * 80)

    client = ATGAPIClient()
    next_saturday = client.get_next_saturday()

    game = client.get_v75_game_for_date(next_saturday)

    if not game or not game.races:
        print("Could not fetch game data")
        return

    # Analyze first race
    race = game.races[0]
    print(f"Race: {race.name}")
    print(f"Distance: {race.distance}m\n")

    # Sort horses by earnings
    horses_with_earnings = [
        (start.number, start.horse.name, start.horse.money)
        for start in race.starts
        if start.horse
    ]

    horses_with_earnings.sort(key=lambda x: x[2], reverse=True)

    print("Top 5 Earners:")
    for i, (number, name, earnings) in enumerate(horses_with_earnings[:5], 1):
        print(f"{i}. #{number} {name}: {earnings:,} SEK")


def example_5_compare_drivers():
    """
    Example 5: Compare drivers in a race
    """
    print("\nExample 5: Compare Drivers")
    print("=" * 80)

    client = ATGAPIClient()
    next_saturday = client.get_next_saturday()

    game = client.get_v75_game_for_date(next_saturday)

    if not game or not game.races:
        print("Could not fetch game data")
        return

    race = game.races[0]
    print(f"Race: {race.name}\n")

    # Group horses by driver
    drivers = {}
    for start in race.starts:
        if start.driver and start.horse:
            driver_name = start.driver.full_name
            if driver_name not in drivers:
                drivers[driver_name] = []
            drivers[driver_name].append({
                'number': start.number,
                'horse': start.horse.name,
                'earnings': start.horse.money
            })

    print("Drivers in this race:")
    for driver_name, horses in sorted(drivers.items()):
        total_earnings = sum(h['earnings'] for h in horses)
        print(f"\n{driver_name}:")
        for h in horses:
            print(f"  #{h['number']} {h['horse']}: {h['earnings']:,} SEK")
        print(f"  Total horse earnings: {total_earnings:,} SEK")


def example_6_race_analysis():
    """
    Example 6: Statistical analysis of a race
    """
    print("\nExample 6: Race Statistical Analysis")
    print("=" * 80)

    client = ATGAPIClient()
    next_saturday = client.get_next_saturday()

    game = client.get_v75_game_for_date(next_saturday)

    if not game or not game.races:
        print("Could not fetch game data")
        return

    race = game.races[0]
    print(f"Race: {race.name}")
    print(f"Distance: {race.distance}m")
    print(f"Start Method: {race.start_method.value if race.start_method else 'Unknown'}\n")

    # Calculate statistics
    earnings_list = [
        start.horse.money for start in race.starts
        if start.horse
    ]

    if not earnings_list:
        print("No horse data available")
        return

    avg_earnings = sum(earnings_list) / len(earnings_list)
    max_earnings = max(earnings_list)
    min_earnings = min(earnings_list)

    print(f"Statistics for {len(earnings_list)} horses:")
    print(f"  Average earnings: {avg_earnings:,.0f} SEK")
    print(f"  Highest earnings: {max_earnings:,} SEK")
    print(f"  Lowest earnings: {min_earnings:,} SEK")
    print(f"  Earnings range: {max_earnings - min_earnings:,} SEK")

    # Find horses above/below average
    above_avg = sum(1 for e in earnings_list if e > avg_earnings)
    below_avg = sum(1 for e in earnings_list if e < avg_earnings)

    print(f"\n  Horses above average: {above_avg}")
    print(f"  Horses below average: {below_avg}")

    # Show field strength
    strong_horses = sum(1 for e in earnings_list if e > avg_earnings * 1.5)
    print(f"  Strong contenders (>150% avg): {strong_horses}")


def example_7_nationality_distribution():
    """
    Example 7: Analyze nationality distribution
    """
    print("\nExample 7: Nationality Distribution")
    print("=" * 80)

    client = ATGAPIClient()
    next_saturday = client.get_next_saturday()

    game = client.get_v75_game_for_date(next_saturday)

    if not game:
        print("Could not fetch game data")
        return

    # Count nationalities across all races
    nationality_count = {}

    for race in game.races:
        for start in race.starts:
            if start.horse:
                nat = start.horse.get_nationality()
                nationality_count[nat] = nationality_count.get(nat, 0) + 1

    print(f"Nationality distribution across {len(game.races)} races:")
    for nat, count in sorted(nationality_count.items(),
                             key=lambda x: x[1],
                             reverse=True):
        print(f"  {nat}: {count} horses")


def example_8_mock_data():
    """
    Example 8: Working with mock data when API is unavailable
    """
    print("\nExample 8: Mock Data Example")
    print("=" * 80)

    # Create mock objects using dataclasses
    from models import (
        Horse, Driver, Trainer, RaceStart, Race,
        Pedigree, HorseSex, StartMethod
    )

    # Create a mock horse
    horse = Horse(
        id=789012,
        name="Global Trustworthy",
        nationality="SE",
        money=1234567,
        age=5,
        sex=HorseSex.GELDING,
        pedigree=Pedigree(
            father=Pedigree.PedigreeHorse(
                id=555666,
                name="Muscle Hill",
                nationality="US"
            ),
            mother=Pedigree.PedigreeHorse(
                id=666777,
                name="Lucky Mare",
                nationality="SE"
            )
        )
    )

    # Create mock driver and trainer
    driver = Driver(
        id=234567,
        first_name="Örjan",
        last_name="Kihlström"
    )

    trainer = Trainer(
        id=123456,
        first_name="Anders",
        last_name="Svanstedt"
    )

    # Create race start
    race_start = RaceStart(
        number=1,
        horse=horse,
        driver=driver,
        trainer=trainer
    )

    # Create race
    race = Race(
        id="2025-10-25_32_5",
        number=5,
        name="Storängens Lopp",
        date="2025-10-25",
        scheduled_start_time="2025-10-25T19:00:00",
        distance=2140,
        start_method=StartMethod.AUTO,
        starts=[race_start]
    )

    # Now you can work with type-safe objects
    print(f"Race: {race.name}")
    print(f"Distance: {race.distance}m")
    print(f"\nHorse #1:")
    print(f"  Name: {horse.name}")
    print(f"  Nationality: {horse.get_nationality()}")
    print(f"  Earnings: {horse.money:,} SEK")
    print(f"  Driver: {driver.full_name}")
    print(f"  Trainer: {trainer.full_name}")

    if horse.pedigree and horse.pedigree.father:
        print(f"  Sire: {horse.pedigree.father.name} ({horse.pedigree.father.nationality})")


def main():
    """
    Run all examples

    Note: Most examples will fail if the API is restricted (403),
    but they demonstrate the intended usage patterns.
    """
    print("ATG API Client - Usage Examples")
    print("=" * 80)
    print("\nNote: Examples may fail if API access is restricted.")
    print("See example_8_mock_data() for working with mock data.\n")

    try:
        example_1_get_next_v75()
    except Exception as e:
        print(f"Example 1 failed: {e}")

    try:
        example_2_analyze_game()
    except Exception as e:
        print(f"Example 2 failed: {e}")

    try:
        example_3_horse_details()
    except Exception as e:
        print(f"Example 3 failed: {e}")

    try:
        example_4_find_top_earners()
    except Exception as e:
        print(f"Example 4 failed: {e}")

    try:
        example_5_compare_drivers()
    except Exception as e:
        print(f"Example 5 failed: {e}")

    try:
        example_6_race_analysis()
    except Exception as e:
        print(f"Example 6 failed: {e}")

    try:
        example_7_nationality_distribution()
    except Exception as e:
        print(f"Example 7 failed: {e}")

    # This one always works
    example_8_mock_data()

    print("\n" + "=" * 80)
    print("Examples complete")
    print("\nFor more information, see:")
    print("- models.py: Data model definitions")
    print("- api_client.py: API client implementation")
    print("- API_EXPLORATION_REPORT.md: Complete API documentation")


if __name__ == "__main__":
    main()
