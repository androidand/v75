# V75 System Implementation Guide

## Quick Start

This guide will help you get started with implementing the V75 betting analysis system based on the proposed architecture.

## Current Situation

### What We Have
1. Basic data fetching from ATG API (currently returning 403)
2. V75 race listing functionality
3. Horse nationality resolution
4. Simple race display

### What We Need
1. Multi-source data collection (fallback to scraping)
2. Database for persistent storage
3. Feature engineering pipeline
4. ML models for predictions
5. Betting strategy system
6. Backtesting framework

## Implementation Steps

### Step 1: Fix Data Access (CRITICAL)

The ATG API is currently returning 403 Forbidden. We need alternative approaches:

#### Option A: Browser Automation

```python
# Install: pip install playwright
# Setup: playwright install chromium

from playwright.async_api import async_playwright

async def fetch_with_browser(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Set Swedish locale
        await page.set_extra_http_headers({
            "Accept-Language": "sv-SE,sv;q=0.9"
        })

        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        # Extract JSON response
        content = await page.content()
        data = await page.evaluate("() => window.__INITIAL_DATA__")

        await browser.close()
        return data
```

#### Option B: Web Scraping

```python
from bs4 import BeautifulSoup
import requests

def scrape_atg_website(date: str):
    """
    Scrape data directly from ATG website
    """
    url = f"https://www.atg.se/spel/v75/{date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract race data from HTML
    # Note: This requires reverse engineering the website structure
    races = []
    # ... parsing logic ...

    return races
```

#### Option C: Third-Party APIs

```python
# Alternative data sources

# 1. Travsport.se (Official Swedish trotting)
def fetch_from_travsport(date: str):
    url = f"https://travsport.se/api/calendar/{date}"
    # May require different approach

# 2. Kanal75 (Statistics and analysis)
def fetch_from_kanal75(date: str):
    url = f"https://www.kanal75.se/v75/{date}"
    # Web scraping likely needed
```

### Step 2: Setup Database

```bash
# Install PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# macOS:
brew install postgresql

# Start PostgreSQL service
sudo service postgresql start

# Create database
sudo -u postgres psql
CREATE DATABASE v75_db;
CREATE USER v75_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE v75_db TO v75_user;
```

```python
# src/database/models.py

from sqlalchemy import create_engine, Column, Integer, String, Date, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Horse(Base):
    __tablename__ = 'horses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nationality = Column(String(2))
    birth_date = Column(Date)
    sex = Column(String(10))

    # Relationships
    starts = relationship("RaceStart", back_populates="horse")
    results = relationship("Result", back_populates="horse")

class Race(Base):
    __tablename__ = 'races'

    id = Column(String, primary_key=True)
    date = Column(Date, nullable=False, index=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    race_number = Column(Integer)
    distance = Column(Integer)
    start_method = Column(String(10))

    # Relationships
    track = relationship("Track")
    starts = relationship("RaceStart", back_populates="race")

class RaceStart(Base):
    __tablename__ = 'race_starts'

    id = Column(Integer, primary_key=True)
    race_id = Column(String, ForeignKey('races.id'))
    horse_id = Column(Integer, ForeignKey('horses.id'))
    start_number = Column(Integer)
    driver_id = Column(Integer, ForeignKey('drivers.id'))
    trainer_id = Column(Integer, ForeignKey('trainers.id'))

    # Relationships
    race = relationship("Race", back_populates="starts")
    horse = relationship("Horse", back_populates="starts")
    driver = relationship("Driver")
    trainer = relationship("Trainer")

class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    race_id = Column(String, ForeignKey('races.id'))
    horse_id = Column(Integer, ForeignKey('horses.id'))
    finish_position = Column(Integer)
    finish_time = Column(Float)
    odds = Column(Float)
    disqualified = Column(Boolean, default=False)

    # Relationships
    horse = relationship("Horse", back_populates="results")

# Create engine and tables
engine = create_engine('postgresql://v75_user:your_password@localhost/v75_db')
Base.metadata.create_all(engine)
```

### Step 3: Refactor Data Collection

```python
# src/data_collection/collectors/race_collector.py

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DataSource(ABC):
    """Abstract base class for data sources"""

    @abstractmethod
    async def fetch_race_day(self, date: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

class ATGAPISource(DataSource):
    """ATG Official API (currently unavailable)"""

    async def fetch_race_day(self, date: str) -> Optional[Dict]:
        # Original API code here
        pass

    def is_available(self) -> bool:
        # Test if API is accessible
        try:
            response = self.test_connection()
            return response.status_code == 200
        except:
            return False

class ATGWebScraperSource(DataSource):
    """Fallback web scraper"""

    async def fetch_race_day(self, date: str) -> Optional[Dict]:
        # Browser automation or BeautifulSoup scraping
        pass

    def is_available(self) -> bool:
        return True  # Web scraping always available

class RaceDataCollector:
    """Orchestrates data collection from multiple sources"""

    def __init__(self):
        self.sources = [
            ATGAPISource(priority=1),
            ATGWebScraperSource(priority=2),
        ]

    async def collect_race_day(self, date: str) -> Dict:
        """
        Collect race data with automatic fallback
        """
        for source in sorted(self.sources, key=lambda x: x.priority):
            if not source.is_available():
                logger.warning(f"{source.__class__.__name__} not available")
                continue

            try:
                data = await source.fetch_race_day(date)
                if data and self.validate_data(data):
                    logger.info(f"Data collected from {source.__class__.__name__}")
                    return data
            except Exception as e:
                logger.error(f"{source.__class__.__name__} failed: {e}")
                continue

        raise Exception("All data sources failed")

    def validate_data(self, data: Dict) -> bool:
        """Validate data structure"""
        required_keys = ['date', 'tracks', 'games']
        return all(key in data for key in required_keys)
```

### Step 4: Feature Engineering

```python
# src/analysis/features/horse_features.py

import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta

class HorseFeatureExtractor:
    """Extract features for a horse in a race"""

    def __init__(self, db_session):
        self.session = db_session

    def extract_features(self,
                        horse_id: int,
                        race_date: datetime,
                        track_id: int,
                        distance: int) -> Dict:
        """
        Extract all features for a horse
        """
        # Get historical results (only before race_date)
        results = self.get_historical_results(horse_id, race_date)

        features = {}

        # Recent form features
        features.update(self.calculate_recent_form(results, races=5))
        features.update(self.calculate_recent_form(results, races=10))

        # Track-specific features
        features.update(self.calculate_track_stats(results, track_id))

        # Distance-specific features
        features.update(self.calculate_distance_stats(results, distance))

        # Time-based features
        features.update(self.calculate_time_features(results, race_date))

        # Career statistics
        features.update(self.calculate_career_stats(results))

        return features

    def calculate_recent_form(self, results: List, races: int = 5) -> Dict:
        """Calculate recent form statistics"""
        recent = results[:races]

        if not recent:
            return {
                f'win_rate_last_{races}': 0.0,
                f'place_rate_last_{races}': 0.0,
                f'avg_finish_last_{races}': 7.0,
            }

        wins = sum(1 for r in recent if r.finish_position == 1)
        places = sum(1 for r in recent if r.finish_position <= 3)
        avg_finish = sum(r.finish_position for r in recent) / len(recent)

        return {
            f'win_rate_last_{races}': wins / len(recent),
            f'place_rate_last_{races}': places / len(recent),
            f'avg_finish_last_{races}': avg_finish,
        }

    def calculate_track_stats(self, results: List, track_id: int) -> Dict:
        """Calculate performance at specific track"""
        track_results = [r for r in results if r.race.track_id == track_id]

        if not track_results:
            return {
                'track_starts': 0,
                'track_win_rate': 0.0,
                'track_place_rate': 0.0,
            }

        wins = sum(1 for r in track_results if r.finish_position == 1)
        places = sum(1 for r in track_results if r.finish_position <= 3)

        return {
            'track_starts': len(track_results),
            'track_win_rate': wins / len(track_results),
            'track_place_rate': places / len(track_results),
        }

    # More feature calculation methods...
```

### Step 5: Build ML Model

```python
# src/analysis/models/predictor.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

class RacePredictor:
    """ML model for predicting race outcomes"""

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        self.feature_columns = None

    def prepare_training_data(self, races: List) -> pd.DataFrame:
        """
        Prepare training data from historical races
        """
        feature_extractor = HorseFeatureExtractor(db_session)

        data = []
        for race in races:
            for start in race.starts:
                features = feature_extractor.extract_features(
                    horse_id=start.horse_id,
                    race_date=race.date,
                    track_id=race.track_id,
                    distance=race.distance
                )

                # Add target variable (did horse win?)
                result = start.result
                features['won'] = 1 if result.finish_position == 1 else 0

                data.append(features)

        df = pd.DataFrame(data)
        return df

    def train(self, training_races: List):
        """Train the model"""
        df = self.prepare_training_data(training_races)

        # Separate features and target
        X = df.drop(['won'], axis=1)
        y = df['won']

        # Store feature columns
        self.feature_columns = X.columns.tolist()

        # Train model
        self.model.fit(X, y)

    def predict_race(self, race_starts: List) -> pd.DataFrame:
        """
        Predict outcomes for a race
        """
        feature_extractor = HorseFeatureExtractor(db_session)

        features_list = []
        for start in race_starts:
            features = feature_extractor.extract_features(
                horse_id=start.horse_id,
                race_date=start.race.date,
                track_id=start.race.track_id,
                distance=start.race.distance
            )
            features['start_number'] = start.start_number
            features_list.append(features)

        df = pd.DataFrame(features_list)
        X = df[self.feature_columns]

        # Get win probabilities
        probabilities = self.model.predict_proba(X)[:, 1]

        # Return predictions
        df['win_probability'] = probabilities
        return df[['start_number', 'win_probability']]

    def save(self, filepath: str):
        """Save model to disk"""
        joblib.dump({
            'model': self.model,
            'feature_columns': self.feature_columns
        }, filepath)

    def load(self, filepath: str):
        """Load model from disk"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.feature_columns = data['feature_columns']
```

### Step 6: Betting Strategy

```python
# src/strategy/systems/value_betting.py

class ValueBettingStrategy:
    """Find value bets based on model predictions"""

    def __init__(self, edge_threshold: float = 0.05):
        self.edge_threshold = edge_threshold

    def analyze_race(self,
                    predictions: pd.DataFrame,
                    odds: Dict[int, float]) -> List[Dict]:
        """
        Find value bets in a race
        """
        value_bets = []

        for _, row in predictions.iterrows():
            start_number = row['start_number']
            predicted_prob = row['win_probability']
            horse_odds = odds.get(start_number, 1.0)

            # Calculate market probability
            market_prob = 1 / horse_odds

            # Calculate edge
            edge = predicted_prob - market_prob

            if edge > self.edge_threshold:
                value_bets.append({
                    'start_number': start_number,
                    'predicted_probability': predicted_prob,
                    'market_probability': market_prob,
                    'odds': horse_odds,
                    'edge': edge,
                    'expected_value': predicted_prob * horse_odds - 1
                })

        return sorted(value_bets, key=lambda x: x['edge'], reverse=True)

    def generate_v75_system(self,
                           race_predictions: List[pd.DataFrame],
                           budget: int = 500) -> Dict:
        """
        Generate V75 betting system
        """
        # Identify top horses in each race
        selections = {}
        for race_num, predictions in enumerate(race_predictions, 1):
            # Take top 3 horses by probability
            top_horses = predictions.nlargest(3, 'win_probability')
            selections[race_num] = top_horses['start_number'].tolist()

        # Generate combinations
        total_combinations = 1
        for horses in selections.values():
            total_combinations *= len(horses)

        cost_per_combo = 1  # SEK
        total_cost = total_combinations * cost_per_combo

        # If over budget, reduce selections
        while total_cost > budget:
            # Remove least probable selection from race with most selections
            max_race = max(selections.items(),
                          key=lambda x: len(x[1]))[0]
            selections[max_race] = selections[max_race][:-1]

            total_combinations = 1
            for horses in selections.values():
                total_combinations *= len(horses)
            total_cost = total_combinations * cost_per_combo

        return {
            'selections': selections,
            'combinations': total_combinations,
            'cost': total_cost,
            'expected_probability': self.calculate_system_probability(
                race_predictions, selections
            )
        }
```

### Step 7: Backtesting

```python
# src/evaluation/backtesting.py

from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd

class Backtester:
    """Backtest betting strategies"""

    def __init__(self, strategy, predictor, db_session):
        self.strategy = strategy
        self.predictor = predictor
        self.session = db_session

    def run_backtest(self,
                    start_date: str,
                    end_date: str,
                    initial_bankroll: float = 10000) -> pd.DataFrame:
        """
        Run backtest over date range
        """
        results = []
        bankroll = initial_bankroll

        # Get all V75 games in period
        games = self.get_v75_games(start_date, end_date)

        for game in games:
            # Train model on data before this date
            training_races = self.get_training_data(
                end_date=game.date - timedelta(days=1)
            )
            self.predictor.train(training_races)

            # Make predictions for each race
            race_predictions = []
            for race in game.races:
                predictions = self.predictor.predict_race(race.starts)
                race_predictions.append(predictions)

            # Generate betting system
            betting_system = self.strategy.generate_v75_system(
                race_predictions,
                budget=bankroll * 0.05  # Bet 5% of bankroll
            )

            # Get actual results
            actual_result = self.get_game_result(game.id)

            # Calculate payout
            payout = self.calculate_payout(
                betting_system['selections'],
                actual_result
            )

            # Update bankroll
            bankroll += payout - betting_system['cost']

            results.append({
                'date': game.date,
                'cost': betting_system['cost'],
                'payout': payout,
                'profit': payout - betting_system['cost'],
                'bankroll': bankroll,
                'roi': (payout - betting_system['cost']) / betting_system['cost']
            })

        return pd.DataFrame(results)

    def calculate_payout(self,
                        selections: Dict,
                        result: List[int]) -> float:
        """
        Calculate payout for betting system
        """
        # Check if all selections are correct
        for race_num, winner in enumerate(result, 1):
            if winner not in selections.get(race_num, []):
                return 0.0

        # All correct - get payout from odds/pool
        # This requires historical payout data
        return self.get_historical_payout(selections, result)
```

### Step 8: Create Simple CLI

```python
# cli.py

import click
from src.data_collection.collectors import RaceDataCollector
from src.analysis.models import RacePredictor
from src.strategy.systems import ValueBettingStrategy

@click.group()
def cli():
    """V75 Betting Analysis System"""
    pass

@cli.command()
@click.argument('date')
def collect(date):
    """Collect race data for date"""
    collector = RaceDataCollector()
    data = collector.collect_race_day(date)
    click.echo(f"Collected data for {date}")

@cli.command()
@click.argument('date')
def predict(date):
    """Generate predictions for date"""
    predictor = RacePredictor()
    predictor.load('models/latest.pkl')

    races = get_races_for_date(date)
    for race in races:
        predictions = predictor.predict_race(race.starts)
        click.echo(f"\nRace {race.race_number}:")
        click.echo(predictions.to_string())

@cli.command()
@click.argument('date')
@click.option('--budget', default=500, help='Betting budget')
def system(date, budget):
    """Generate betting system"""
    predictor = RacePredictor()
    predictor.load('models/latest.pkl')
    strategy = ValueBettingStrategy()

    # Get predictions for all races
    races = get_races_for_date(date)
    race_predictions = [predictor.predict_race(r.starts) for r in races]

    # Generate system
    betting_system = strategy.generate_v75_system(
        race_predictions,
        budget=budget
    )

    click.echo("V75 System:")
    for race_num, selections in betting_system['selections'].items():
        click.echo(f"Race {race_num}: {', '.join(map(str, selections))}")
    click.echo(f"\nTotal combinations: {betting_system['combinations']}")
    click.echo(f"Cost: {betting_system['cost']} SEK")

if __name__ == '__main__':
    cli()
```

## Next Steps

1. **Fix Data Access**
   - Implement browser automation or web scraping
   - Test with recent V75 games

2. **Collect Historical Data**
   - Scrape 2-3 years of race results
   - Store in database

3. **Build Features**
   - Implement feature extraction
   - Validate feature quality

4. **Train Models**
   - Create training pipeline
   - Evaluate model performance

5. **Backtest Strategies**
   - Test different betting systems
   - Measure performance metrics

6. **Deploy**
   - Automate weekly predictions
   - Monitor performance

## Resources

### Swedish Horse Racing
- ATG: https://www.atg.se
- Travsport: https://travsport.se
- Kanal75: https://www.kanal75.se

### Machine Learning
- Scikit-learn: https://scikit-learn.org
- XGBoost: https://xgboost.readthedocs.io
- Feature Engineering: https://www.kaggle.com/learn/feature-engineering

### Betting Strategy
- Kelly Criterion: https://en.wikipedia.org/wiki/Kelly_criterion
- Value Betting: https://www.pinnacle.com/en/betting-articles/Betting-Strategy/what-is-value-betting

## Legal Disclaimer

This system is for educational and research purposes only. Always:
- Check local laws regarding betting
- Never bet more than you can afford to lose
- Be aware of gambling addiction risks
- Respect ATG's terms of service

Past performance does not guarantee future results.
