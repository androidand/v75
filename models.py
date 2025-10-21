"""
ATG Racing Information API - Data Models

This module defines typed dataclasses for all ATG API responses.
Based on reverse engineering of the ATG Racing Information v1 API.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


# Enumerations

class StartMethod(str, Enum):
    """Race start method"""
    AUTO = "auto"  # Car start (autostart)
    VOLT = "volt"  # Standing start (voltstart)


class GameType(str, Enum):
    """ATG game types"""
    V75 = "V75"
    V86 = "V86"
    V64 = "V64"
    V65 = "V65"
    GS75 = "GS75"
    V4 = "V4"
    V3 = "V3"


class HorseSex(str, Enum):
    """Horse sex/gender"""
    STALLION = "stallion"
    MARE = "mare"
    GELDING = "gelding"


class GameStatus(str, Enum):
    """Game status"""
    UPCOMING = "upcoming"
    OPEN = "open"
    CLOSED = "closed"
    RESULTS = "results"


# Basic entities

@dataclass
class Person:
    """Represents a person (driver, trainer, breeder)"""
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""

    @property
    def full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class Driver(Person):
    """Horse driver"""
    license_year: Optional[int] = None
    short_name: Optional[str] = None


@dataclass
class Trainer(Person):
    """Horse trainer"""
    location: Optional[str] = None
    stable: Optional[str] = None


@dataclass
class Pedigree:
    """Horse pedigree information"""

    @dataclass
    class PedigreeHorse:
        """A horse in pedigree"""
        id: Optional[int] = None
        name: str = ""
        nationality: Optional[str] = None

    father: Optional[PedigreeHorse] = None
    mother: Optional[PedigreeHorse] = None
    grandfather: Optional[PedigreeHorse] = None  # Mother's father

    def get_nationality(self) -> Optional[str]:
        """Get nationality from pedigree (father > mother > grandfather)"""
        if self.father and self.father.nationality:
            return self.father.nationality
        if self.mother and self.mother.nationality:
            return self.mother.nationality
        if self.grandfather and self.grandfather.nationality:
            return self.grandfather.nationality
        return None


@dataclass
class Horse:
    """Horse information"""
    id: int
    name: str
    nationality: Optional[str] = None
    money: int = 0  # Career earnings in SEK
    age: Optional[int] = None
    sex: Optional[HorseSex] = None
    birth_date: Optional[str] = None
    pedigree: Optional[Pedigree] = None

    def get_nationality(self) -> str:
        """Get horse nationality with fallback to pedigree"""
        if self.nationality:
            return self.nationality
        if self.pedigree:
            pedigree_nat = self.pedigree.get_nationality()
            if pedigree_nat:
                return pedigree_nat
        return "Unknown"


@dataclass
class RaceStart:
    """A horse's participation in a race"""
    number: int  # Starting position/number
    post_position: Optional[int] = None  # Actual post position
    distance: Optional[int] = None  # Handicap distance
    horse: Optional[Horse] = None
    driver: Optional[Driver] = None
    trainer: Optional[Trainer] = None

    # Additional racing information
    scratched: bool = False
    disqualified: bool = False
    galloped: bool = False

    # Betting related
    odds: Optional[float] = None
    odds_change: Optional[float] = None

    # Results
    finish_position: Optional[int] = None
    finish_time: Optional[str] = None
    km_time: Optional[str] = None  # Time per kilometer
    prize: Optional[int] = None


@dataclass
class Track:
    """Racing track information"""
    id: int
    name: str
    country: str = "SE"
    biggest_game_type: Optional[GameType] = None
    location: Optional[str] = None

    # Track characteristics
    surface: Optional[str] = None  # e.g., "sand", "grass"
    length: Optional[int] = None  # Track length in meters


@dataclass
class Race:
    """Individual race information"""
    id: str  # Format: YYYY-MM-DD_track-id_race-number
    number: int
    name: str
    date: str

    # Timing
    scheduled_start_time: str  # ISO 8601 format
    start_time: Optional[str] = None  # Actual start time
    post_time: Optional[str] = None

    # Race details
    distance: int = 0  # meters
    start_method: Optional[StartMethod] = None
    track_id: Optional[int] = None
    track: Optional[Track] = None

    # Race conditions
    monte: bool = False  # Mounted race (ridden)
    conditions: Optional[str] = None
    prize: Optional[int] = None

    # Participants
    starts: List[RaceStart] = field(default_factory=list)

    # Results
    result: Optional[List[int]] = None  # Finish order by start number

    @property
    def start_time_dt(self) -> Optional[datetime]:
        """Get start time as datetime"""
        try:
            return datetime.fromisoformat(self.scheduled_start_time.replace('Z', '+00:00'))
        except:
            return None


@dataclass
class GameInfo:
    """V75/V86 game information"""
    id: str  # Format: V75_YYYY-MM-DD_track-id_race-number
    type: GameType
    races: List[str] = field(default_factory=list)  # List of race IDs
    turnover: Optional[int] = None
    jackpot: Optional[int] = None


@dataclass
class Game:
    """Complete game data with all races"""
    id: str
    type: GameType
    status: GameStatus = GameStatus.UPCOMING

    # Game details
    races: List[Race] = field(default_factory=list)

    # Betting pools
    pools: Optional[Dict] = None
    turnover: Optional[int] = None

    # Results
    result: Optional[List[int]] = None  # Winning numbers
    results: Optional[Dict] = None  # Detailed results by bet type
    payouts: Optional[Dict] = None  # Payouts by bet type

    @property
    def race_ids(self) -> List[str]:
        """Get list of race IDs"""
        return [race.id for race in self.races]


@dataclass
class RaceDay:
    """Race day calendar data"""
    date: str  # YYYY-MM-DD
    tracks: List[Track] = field(default_factory=list)
    games: Dict[str, List[GameInfo]] = field(default_factory=dict)  # GameType -> List[GameInfo]

    def get_v75_games(self) -> List[GameInfo]:
        """Get all V75 games for this day"""
        return self.games.get("V75", [])

    def get_v75_track(self) -> Optional[Track]:
        """Get the track hosting V75"""
        for track in self.tracks:
            if track.biggest_game_type == GameType.V75:
                return track
        return None


# Results and statistics

@dataclass
class RaceResult:
    """Race result details"""
    race_id: str
    winner: int  # Start number
    finish_order: List[int]  # Start numbers in finish order

    # Exotic results
    exacta: Optional[List[int]] = None  # [1st, 2nd]
    trifecta: Optional[List[int]] = None  # [1st, 2nd, 3rd]
    superfecta: Optional[List[int]] = None  # [1st, 2nd, 3rd, 4th]

    # Timing
    winning_time: Optional[str] = None
    km_time: Optional[str] = None

    # Payouts
    win_payout: Optional[float] = None
    place_payouts: Optional[List[float]] = None
    show_payouts: Optional[List[float]] = None


@dataclass
class GameResult:
    """Game result with payouts"""
    game_id: str
    game_type: GameType
    date: str

    # Results
    winning_numbers: List[int]  # Start numbers for each race
    race_results: List[RaceResult] = field(default_factory=list)

    # Payouts
    seven_right: Optional['Payout'] = None
    six_right: Optional['Payout'] = None
    five_right: Optional['Payout'] = None

    @dataclass
    class Payout:
        """Payout information"""
        winners: int  # Number of winning tickets
        payout: float  # Payout per SEK wagered
        turnover: Optional[int] = None


# Historical statistics

@dataclass
class HorseStatistics:
    """Historical statistics for a horse"""
    horse_id: int

    # Career stats
    starts: int = 0
    wins: int = 0
    places: int = 0  # Top 3
    shows: int = 0  # Top 5

    # Earnings
    total_earnings: int = 0
    earnings_per_start: float = 0.0

    # Performance metrics
    win_percentage: float = 0.0
    place_percentage: float = 0.0

    # Best times
    best_time: Optional[str] = None
    best_km_time: Optional[str] = None

    # Recent form (last 5 starts)
    recent_starts: int = 0
    recent_wins: int = 0
    recent_places: int = 0

    @property
    def form_string(self) -> str:
        """Get form string like '1-3-2-1-4' """
        # Would need recent results to calculate
        return ""


@dataclass
class DriverStatistics:
    """Driver statistics"""
    driver_id: int

    # Career
    starts: int = 0
    wins: int = 0
    win_percentage: float = 0.0

    # Current year
    year_starts: int = 0
    year_wins: int = 0
    year_win_percentage: float = 0.0


@dataclass
class TrainerStatistics:
    """Trainer statistics"""
    trainer_id: int

    # Career
    starts: int = 0
    wins: int = 0
    win_percentage: float = 0.0

    # Current year
    year_starts: int = 0
    year_wins: int = 0
    year_win_percentage: float = 0.0


# API Response wrappers

@dataclass
class CalendarDayResponse:
    """Response from /api/calendar/day/{date}"""
    date: str
    tracks: List[Track] = field(default_factory=list)
    games: Dict[str, List[GameInfo]] = field(default_factory=dict)


@dataclass
class GameResponse:
    """Response from /api/games/{game_id}"""
    id: str
    status: GameStatus
    races: List[Race] = field(default_factory=list)
    pools: Optional[Dict] = None
    results: Optional[Dict] = None


@dataclass
class HorseResponse:
    """Response from /api/horses/{horse_id}"""
    id: int
    name: str
    nationality: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[HorseSex] = None
    money: int = 0
    pedigree: Optional[Pedigree] = None
    record: Optional[str] = None
    breeder: Optional[str] = None


# Helper functions for parsing

def parse_race_day(data: dict) -> RaceDay:
    """Parse race day data from API response"""
    from typing import cast

    tracks = []
    for track_data in data.get('tracks', []):
        track = Track(
            id=track_data['id'],
            name=track_data['name'],
            biggest_game_type=track_data.get('biggestGameType')
        )
        tracks.append(track)

    games = {}
    games_data = data.get('games', {})
    for game_type, game_list in games_data.items():
        games[game_type] = [
            GameInfo(
                id=g['id'],
                type=GameType(game_type),
                races=g.get('races', [])
            )
            for g in game_list
        ]

    return RaceDay(
        date=data['date'],
        tracks=tracks,
        games=games
    )


def parse_horse(data: dict) -> Horse:
    """Parse horse data from API response"""
    pedigree = None
    if 'pedigree' in data:
        p = data['pedigree']
        pedigree = Pedigree(
            father=Pedigree.PedigreeHorse(**p['father']) if 'father' in p else None,
            mother=Pedigree.PedigreeHorse(**p['mother']) if 'mother' in p else None,
            grandfather=Pedigree.PedigreeHorse(**p['grandfather']) if 'grandfather' in p else None
        )

    return Horse(
        id=data['id'],
        name=data['name'],
        nationality=data.get('nationality'),
        money=data.get('money', 0),
        age=data.get('age'),
        pedigree=pedigree
    )


def parse_race(data: dict) -> Race:
    """Parse race data from API response"""
    starts = []
    for start_data in data.get('starts', []):
        horse_data = start_data.get('horse', {})
        driver_data = start_data.get('driver', {})
        trainer_data = start_data.get('trainer', {})

        start = RaceStart(
            number=start_data['number'],
            horse=parse_horse(horse_data) if horse_data else None,
            driver=Driver(
                id=driver_data.get('id'),
                first_name=driver_data.get('firstName', ''),
                last_name=driver_data.get('lastName', '')
            ) if driver_data else None,
            trainer=Trainer(
                id=trainer_data.get('id'),
                first_name=trainer_data.get('firstName', ''),
                last_name=trainer_data.get('lastName', '')
            ) if trainer_data else None
        )
        starts.append(start)

    return Race(
        id=data['id'],
        number=data['number'],
        name=data['name'],
        date=data.get('date', ''),
        scheduled_start_time=data['scheduledStartTime'],
        start_time=data.get('startTime'),
        distance=data.get('distance', 0),
        start_method=StartMethod(data['startMethod']) if 'startMethod' in data else None,
        starts=starts
    )


def parse_game(data: dict) -> Game:
    """Parse complete game data from API response"""
    races = [parse_race(race_data) for race_data in data.get('races', [])]

    return Game(
        id=data['id'],
        type=GameType(data.get('type', 'V75')),
        status=GameStatus(data.get('status', 'upcoming')),
        races=races,
        pools=data.get('pools'),
        results=data.get('results'),
        payouts=data.get('payouts')
    )
