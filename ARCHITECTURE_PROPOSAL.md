# V75 Betting System Architecture Proposal

## Executive Summary

This document proposes a comprehensive architecture for a V75 horse racing analysis and betting system. The system will collect data from multiple sources, analyze historical patterns, apply machine learning models, and generate betting recommendations.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     V75 BETTING SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Data Layer   │  │ Analysis     │  │ Strategy     │         │
│  │              │  │ Layer        │  │ Layer        │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                 │                  │
│  ┌──────▼──────────────────▼─────────────────▼───────┐         │
│  │         Application Services & Orchestration       │         │
│  └───────────────────────────────┬────────────────────┘         │
│                                  │                              │
│  ┌───────────────────────────────▼────────────────────┐         │
│  │         API Gateway / Web Interface                │         │
│  └────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## 1. Project Structure

### Proposed Directory Layout

```
v75-betting-system/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Configuration management
│   │   └── logging_config.py    # Logging setup
│   │
│   ├── data_collection/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── atg_api.py       # ATG API client
│   │   │   ├── alternative_sources.py
│   │   │   └── base_client.py   # Abstract API client
│   │   ├── scrapers/
│   │   │   ├── __init__.py
│   │   │   ├── atg_scraper.py   # Web scraping fallback
│   │   │   ├── travsport_scraper.py
│   │   │   └── kanal75_scraper.py
│   │   └── collectors/
│   │       ├── __init__.py
│   │       ├── race_collector.py
│   │       ├── horse_collector.py
│   │       └── historical_collector.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── race_repository.py
│   │   │   ├── horse_repository.py
│   │   │   └── result_repository.py
│   │   └── migrations/          # Alembic migrations
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── features/
│   │   │   ├── __init__.py
│   │   │   ├── horse_features.py    # Extract horse stats
│   │   │   ├── driver_features.py   # Driver statistics
│   │   │   ├── trainer_features.py  # Trainer patterns
│   │   │   ├── track_features.py    # Track conditions
│   │   │   └── race_features.py     # Race characteristics
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── ml_predictor.py      # ML model interface
│   │   │   ├── random_forest.py     # Random Forest model
│   │   │   ├── xgboost_model.py     # XGBoost model
│   │   │   └── ensemble.py          # Model ensemble
│   │   └── statistics/
│   │       ├── __init__.py
│   │       ├── form_analysis.py     # Recent form
│   │       ├── head_to_head.py      # H2H comparisons
│   │       └── pace_analysis.py     # Race pace patterns
│   │
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── systems/
│   │   │   ├── __init__.py
│   │   │   ├── base_system.py       # Abstract betting system
│   │   │   ├── value_betting.py     # Value bet identification
│   │   │   ├── kelly_criterion.py   # Kelly staking
│   │   │   └── combination_optimizer.py  # Optimize V75 combos
│   │   ├── bankroll/
│   │   │   ├── __init__.py
│   │   │   ├── manager.py           # Bankroll management
│   │   │   └── staking.py           # Staking strategies
│   │   └── optimization/
│   │       ├── __init__.py
│   │       ├── combination_generator.py
│   │       └── cost_optimizer.py    # Minimize bet cost
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── backtesting.py           # Backtest strategies
│   │   ├── metrics.py               # Performance metrics
│   │   └── reporting.py             # Generate reports
│   │
│   └── api/
│       ├── __init__.py
│       ├── main.py                  # FastAPI application
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── predictions.py       # Prediction endpoints
│       │   ├── analysis.py          # Analysis endpoints
│       │   └── admin.py             # Admin functions
│       └── schemas/
│           ├── __init__.py
│           └── models.py            # Pydantic models
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── scripts/
│   ├── collect_data.py              # Data collection script
│   ├── train_models.py              # Model training
│   └── generate_predictions.py      # Weekly predictions
│
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   ├── feature_engineering.ipynb
│   └── model_evaluation.ipynb
│
├── data/
│   ├── raw/                         # Raw API responses
│   ├── processed/                   # Cleaned data
│   ├── features/                    # Feature matrices
│   └── models/                      # Trained models
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   ├── DATA_DICTIONARY.md
│   └── USER_GUIDE.md
│
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
└── README.md
```

## 2. Technology Stack

### Core Technologies

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Language** | Python 3.11+ | Rich ML ecosystem, easy prototyping |
| **Database** | PostgreSQL | Relational data, JSONB support |
| **Cache** | Redis | Fast data access, session storage |
| **Web Framework** | FastAPI | Modern, async, auto-documentation |
| **ORM** | SQLAlchemy | Powerful ORM with migration support |
| **Task Queue** | Celery | Async task processing |
| **ML Framework** | scikit-learn, XGBoost | Proven ML libraries |
| **Data Analysis** | pandas, numpy | Industry standard |
| **Visualization** | plotly, matplotlib | Interactive charts |
| **Web Scraping** | BeautifulSoup4, Selenium | Fallback data collection |
| **Testing** | pytest | Comprehensive testing framework |

### Dependencies

```python
# requirements.txt
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1

# Data Processing
pandas==2.1.3
numpy==1.26.2
scipy==1.11.4

# Machine Learning
scikit-learn==1.3.2
xgboost==2.0.2
lightgbm==4.1.0
optuna==3.4.0  # Hyperparameter optimization

# Data Collection
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
playwright==1.40.0

# Task Processing
celery==5.3.4
flower==2.0.1  # Celery monitoring

# Visualization
plotly==5.18.0
matplotlib==3.8.2
seaborn==0.13.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
faker==20.1.0

# Utilities
python-dateutil==2.8.2
pytz==2023.3
tqdm==4.66.1
loguru==0.7.2
```

## 3. Data Layer Architecture

### 3.1 Database Schema

```python
# Core tables

class Horse(Base):
    """Horse master data"""
    id = Integer (PK)
    name = String
    nationality = String
    birth_date = Date
    sex = String
    sire_id = Integer (FK)
    dam_id = Integer (FK)

class Driver(Base):
    """Driver information"""
    id = Integer (PK)
    first_name = String
    last_name = String
    license_year = Integer

class Trainer(Base):
    """Trainer information"""
    id = Integer (PK)
    first_name = String
    last_name = String
    stable_location = String

class Track(Base):
    """Racing tracks"""
    id = Integer (PK)
    name = String
    location = String
    surface_type = String

class Race(Base):
    """Individual races"""
    id = String (PK)
    date = Date
    track_id = Integer (FK)
    race_number = Integer
    distance = Integer
    start_method = String (auto/volt)
    purse = Integer

class RaceStart(Base):
    """Horse participation in race"""
    race_id = String (FK)
    start_number = Integer
    horse_id = Integer (FK)
    driver_id = Integer (FK)
    trainer_id = Integer (FK)
    post_position = Integer

class Result(Base):
    """Race results"""
    race_id = String (FK)
    horse_id = Integer (FK)
    finish_position = Integer
    time = Decimal
    odds = Decimal
    disqualified = Boolean

class Game(Base):
    """V75/V86 game information"""
    id = String (PK)
    game_type = String
    date = Date
    races = List[String]  # Race IDs
    turnover = Integer

class Payout(Base):
    """Game payouts"""
    game_id = String (FK)
    bet_type = String  # 7-right, 6-right, etc.
    winners = Integer
    payout = Decimal
```

### 3.2 Data Collection Strategy

#### Multi-Source Approach

```python
class DataCollectionOrchestrator:
    """
    Manages data collection from multiple sources with fallback logic
    """

    def __init__(self):
        self.sources = [
            ATGAPISource(priority=1),
            ATGScraperSource(priority=2),
            TravsportSource(priority=3),
            Kanal75Source(priority=4),
        ]

    async def collect_race_data(self, date: str):
        """
        Try each source in priority order until success
        """
        for source in sorted(self.sources, key=lambda x: x.priority):
            try:
                data = await source.fetch_race_day(date)
                if self.validate_data(data):
                    await self.store_data(data)
                    return data
            except Exception as e:
                logger.warning(f"{source.name} failed: {e}")
                continue

        raise DataCollectionError("All sources failed")
```

#### Automated Collection Schedule

```python
# Celery tasks for automated data collection

@celery.schedule(cron_hour=8, cron_day_of_week=6)  # Saturday 08:00
async def collect_weekly_v75():
    """Collect upcoming V75 race data"""
    collector = RaceDataCollector()
    await collector.collect_current_week()

@celery.schedule(cron_hour=22, cron_day_of_week=6)  # Saturday 22:00
async def collect_results():
    """Collect race results after completion"""
    collector = ResultCollector()
    await collector.collect_todays_results()

@celery.schedule(cron_hour=2)  # Daily 02:00
async def collect_historical():
    """Backfill historical data"""
    collector = HistoricalCollector()
    await collector.collect_missing_data()
```

## 4. Analysis Layer

### 4.1 Feature Engineering

Extract meaningful features from raw data:

#### Horse Features
- **Recent Form**: Win rate last 5, 10, 20 races
- **Track Record**: Performance at specific track
- **Distance Performance**: Win rate at race distance
- **Start Method**: Auto vs volt performance
- **Earnings**: Recent and career earnings
- **Days Since Last Race**: Freshness indicator
- **Career Statistics**: Lifetime win%, place%, show%
- **Speed Ratings**: Best times at distance
- **Class Level**: Competition quality indicator

#### Driver Features
- **Win Rate**: Overall and recent
- **Track Expertise**: Performance at track
- **Horse Compatibility**: Success rate with specific horse
- **Position Skills**: Performance from different posts

#### Trainer Features
- **Win Rate**: Overall and recent
- **Stable Form**: Current stable performance
- **Specialty**: Distance/track preferences
- **Peak Timing**: Ability to have horses ready

#### Race Context Features
- **Field Strength**: Quality of competition
- **Pace Scenario**: Expected race pace
- **Post Position**: Starting position advantage
- **Distance**: Race distance
- **Track Condition**: Fast/good/sloppy
- **Weather**: Temperature, wind

#### Combined Features
- **Driver-Trainer Combination**: Partnership success
- **Odds**: Market expectation
- **Public Confidence**: Betting patterns

### 4.2 Machine Learning Models

```python
class PredictionEnsemble:
    """
    Ensemble of multiple ML models for robust predictions
    """

    def __init__(self):
        self.models = {
            'random_forest': RandomForestModel(),
            'xgboost': XGBoostModel(),
            'lightgbm': LightGBMModel(),
            'neural_net': NeuralNetworkModel(),
        }
        self.meta_model = LogisticRegression()

    def train(self, X_train, y_train, X_val, y_val):
        """Train all models and meta-model"""

        # Train base models
        predictions = {}
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            predictions[name] = model.predict_proba(X_val)

        # Train meta-model on base predictions
        meta_features = np.column_stack(list(predictions.values()))
        self.meta_model.fit(meta_features, y_val)

    def predict_proba(self, X):
        """Generate ensemble predictions"""
        predictions = np.column_stack([
            model.predict_proba(X)
            for model in self.models.values()
        ])
        return self.meta_model.predict_proba(predictions)
```

### Target Variables

1. **Win Probability**: P(horse finishes 1st)
2. **Place Probability**: P(horse finishes top 3)
3. **Expected Finish Position**: Regression target
4. **Beat Favorite**: P(horse beats the favorite)

## 5. Strategy Layer

### 5.1 Betting Systems

#### Value Betting System

```python
class ValueBettingSystem:
    """
    Identify bets where our probability > market probability
    """

    def find_value_bets(self, predictions, odds, threshold=0.05):
        """
        Find horses where edge > threshold
        """
        value_bets = []

        for horse, pred_prob in predictions.items():
            market_prob = 1 / odds[horse]
            edge = pred_prob - market_prob

            if edge > threshold:
                value_bets.append({
                    'horse': horse,
                    'predicted_prob': pred_prob,
                    'market_prob': market_prob,
                    'edge': edge,
                    'odds': odds[horse]
                })

        return sorted(value_bets, key=lambda x: x['edge'], reverse=True)
```

#### Kelly Criterion Staking

```python
class KellyStaking:
    """
    Optimal bet sizing using Kelly Criterion
    """

    def calculate_stake(self,
                       bankroll: float,
                       probability: float,
                       odds: float,
                       kelly_fraction: float = 0.25) -> float:
        """
        Kelly formula: f = (bp - q) / b
        where b = odds-1, p = win probability, q = 1-p
        """
        b = odds - 1
        p = probability
        q = 1 - p

        kelly = (b * p - q) / b

        # Use fractional Kelly for safety
        kelly = max(0, kelly * kelly_fraction)

        return bankroll * kelly
```

#### V75 Combination Optimizer

```python
class V75CombinationOptimizer:
    """
    Generate optimal V75 combinations within budget
    """

    def optimize_system(self,
                       predictions: Dict,
                       budget: int,
                       min_probability: float = 0.001):
        """
        Generate combinations using:
        1. Top horses per race
        2. Budget constraint
        3. Probability threshold
        4. Diversity (banker, reserves)
        """

        # Identify bankers (high confidence picks)
        bankers = self.identify_bankers(predictions, threshold=0.40)

        # Build combinations
        if bankers:
            # Use bankers + reserves strategy
            combinations = self.generate_banker_systems(
                bankers, predictions, budget
            )
        else:
            # Full coverage or value-based systems
            combinations = self.generate_coverage_systems(
                predictions, budget
            )

        return self.optimize_cost(combinations, budget)
```

### 5.2 Bankroll Management

```python
class BankrollManager:
    """
    Manage betting bankroll with risk controls
    """

    def __init__(self, initial_bankroll: float):
        self.bankroll = initial_bankroll
        self.max_bet_percentage = 0.05  # Max 5% per bet
        self.max_day_risk = 0.10  # Max 10% per day

    def can_place_bet(self, bet_amount: float) -> bool:
        """Check if bet is within risk limits"""
        return bet_amount <= self.bankroll * self.max_bet_percentage

    def update_bankroll(self, result: float):
        """Update bankroll after bet result"""
        self.bankroll += result
        self.log_transaction(result)
```

## 6. Evaluation & Backtesting

### 6.1 Backtesting Framework

```python
class Backtester:
    """
    Backtest betting strategies on historical data
    """

    def run_backtest(self,
                     strategy: BettingStrategy,
                     start_date: str,
                     end_date: str,
                     initial_bankroll: float):
        """
        Simulate strategy performance over period
        """
        bankroll = initial_bankroll
        results = []

        for game_date in self.date_range(start_date, end_date):
            # Get historical data
            races = self.get_races(game_date)
            odds = self.get_historical_odds(game_date)

            # Generate predictions (using only past data)
            predictions = strategy.predict(races, as_of_date=game_date)

            # Generate bets
            bets = strategy.generate_bets(predictions, odds, bankroll)

            # Get actual results
            results_data = self.get_results(game_date)

            # Calculate returns
            payout = self.calculate_payout(bets, results_data)
            bankroll += payout

            results.append({
                'date': game_date,
                'bets': bets,
                'payout': payout,
                'bankroll': bankroll
            })

        return self.generate_report(results)
```

### 6.2 Performance Metrics

```python
class PerformanceMetrics:
    """
    Calculate strategy performance metrics
    """

    @staticmethod
    def calculate_metrics(results: List[Dict]) -> Dict:
        returns = [r['payout'] - r['bet_amount'] for r in results]

        return {
            'total_return': sum(returns),
            'roi': sum(returns) / sum(r['bet_amount'] for r in results),
            'win_rate': sum(1 for r in returns if r > 0) / len(returns),
            'avg_win': np.mean([r for r in returns if r > 0]),
            'avg_loss': np.mean([r for r in returns if r < 0]),
            'sharpe_ratio': np.mean(returns) / np.std(returns),
            'max_drawdown': self.calculate_max_drawdown(results),
            'profit_factor': sum(r for r in returns if r > 0) /
                           abs(sum(r for r in returns if r < 0)),
        }
```

## 7. API Layer

### 7.1 REST API Endpoints

```python
# FastAPI application

@app.get("/api/v1/predictions/{game_id}")
async def get_predictions(game_id: str):
    """Get predictions for upcoming V75 game"""
    predictions = await prediction_service.generate_predictions(game_id)
    return predictions

@app.get("/api/v1/systems/{game_id}")
async def get_betting_systems(
    game_id: str,
    budget: int = 500,
    strategy: str = "value"
):
    """Get recommended betting systems"""
    systems = await system_service.generate_systems(
        game_id, budget, strategy
    )
    return systems

@app.get("/api/v1/analysis/horse/{horse_id}")
async def get_horse_analysis(horse_id: int):
    """Detailed horse analysis and statistics"""
    analysis = await analysis_service.analyze_horse(horse_id)
    return analysis

@app.post("/api/v1/backtest")
async def run_backtest(config: BacktestConfig):
    """Run strategy backtest"""
    results = await backtest_service.run(config)
    return results
```

## 8. Deployment Architecture

### Development Environment
- Docker Compose for local development
- Hot reload for rapid iteration
- Local PostgreSQL and Redis

### Production Environment
- **Compute**: AWS EC2 / DigitalOcean Droplet
- **Database**: AWS RDS PostgreSQL
- **Cache**: AWS ElastiCache Redis
- **Storage**: AWS S3 for data files
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack
- **CI/CD**: GitHub Actions

### Docker Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/v75
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=v75
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass

  redis:
    image: redis:7-alpine

  celery:
    build: .
    command: celery -A src.tasks worker -l info
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A src.tasks beat -l info
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

## 9. Development Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [ ] Setup project structure
- [ ] Implement database schema
- [ ] Create data collection pipeline
- [ ] Build API client with fallback sources
- [ ] Collect historical data (2+ years)

### Phase 2: Analysis (Weeks 5-8)
- [ ] Feature engineering pipeline
- [ ] Exploratory data analysis
- [ ] Statistical analysis tools
- [ ] Build baseline ML models
- [ ] Model evaluation framework

### Phase 3: Strategy (Weeks 9-12)
- [ ] Implement betting systems
- [ ] Bankroll management
- [ ] Combination optimizer
- [ ] Backtesting framework
- [ ] Performance metrics

### Phase 4: Integration (Weeks 13-16)
- [ ] FastAPI application
- [ ] Web interface (optional)
- [ ] Automated predictions
- [ ] Monitoring and alerting
- [ ] Documentation

### Phase 5: Optimization (Weeks 17-20)
- [ ] Model tuning
- [ ] Strategy refinement
- [ ] Live testing (paper trading)
- [ ] Performance analysis
- [ ] System hardening

## 10. Risk Management

### Technical Risks
- **Data Access**: API may become unavailable
  - *Mitigation*: Multiple data sources, scraping fallback
- **Model Overfitting**: Models perform poorly on new data
  - *Mitigation*: Cross-validation, regularization, out-of-sample testing
- **Data Quality**: Incomplete or incorrect data
  - *Mitigation*: Validation rules, multiple sources, manual checks

### Business Risks
- **Negative Returns**: Strategy loses money
  - *Mitigation*: Strict bankroll management, backtesting, start small
- **Legal Issues**: Terms of service violations
  - *Mitigation*: Review ToS, personal use only, seek legal advice
- **Addiction**: Promoting problem gambling
  - *Mitigation*: Responsible gambling features, limits, warnings

## 11. Success Metrics

### Model Performance
- Prediction accuracy > 35% (race winner)
- Top-3 prediction accuracy > 70%
- Calibration error < 5%

### Betting Performance
- Positive ROI over 100+ games
- Sharpe ratio > 1.0
- Max drawdown < 30%
- Win rate > 40%

### System Performance
- Data collection success rate > 95%
- API response time < 500ms
- System uptime > 99.5%

## Conclusion

This architecture provides a solid foundation for building a comprehensive V75 betting analysis system. The modular design allows for:
- Incremental development
- Easy testing and validation
- Multiple data sources
- Flexible betting strategies
- Robust risk management

The key to success will be:
1. **Quality Data**: Comprehensive, accurate historical data
2. **Rigorous Testing**: Thorough backtesting before live betting
3. **Risk Management**: Never bet more than you can afford to lose
4. **Continuous Improvement**: Learn from results and refine strategies
5. **Responsible Gambling**: Treat this as analytical exercise, not income source

Remember: Past performance doesn't guarantee future results. Always bet responsibly.
