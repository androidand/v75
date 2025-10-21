# V75 Betting Analysis System

A comprehensive system for analyzing Swedish V75 horse racing data and developing betting strategies through data analysis and machine learning.

## Overview

This project aims to:
1. Collect V75 race data from ATG and alternative sources
2. Analyze historical performance patterns
3. Build predictive models using machine learning
4. Generate data-driven betting recommendations
5. Backtest strategies to validate performance

## Project Status

### Current State (v0.1)
- Basic ATG API client implementation
- Race data fetching and display
- Horse nationality resolution with pedigree fallback

### Known Issues
- ATG API currently returns 403 Forbidden (as of October 2025)
- Need alternative data sources (web scraping, third-party APIs)

### Roadmap
See [ARCHITECTURE_PROPOSAL.md](ARCHITECTURE_PROPOSAL.md) for detailed development roadmap.

## Quick Start

### Current Implementation

1. **Install dependencies**:
   ```bash
   pip install requests
   ```

2. **Fetch next V75 game day**:
   ```bash
   python3 v75.py
   ```

3. **Fetch specific date** (YYYY-MM-DD):
   ```bash
   python3 v75.py 2024-10-12
   ```

4. **List all V75 Saturdays**:
   ```bash
   python3 v75.py list-dates
   ```

### Future Implementation

See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for step-by-step implementation instructions.

## Documentation

### Core Documents

| Document | Description |
|----------|-------------|
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete ATG API reference with endpoints, data models, and examples |
| [ARCHITECTURE_PROPOSAL.md](ARCHITECTURE_PROPOSAL.md) | Comprehensive system architecture for betting analysis platform |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | Step-by-step guide for implementing the proposed architecture |

### Key Topics

- **Data Collection**: Multi-source strategy with API, scraping, and third-party sources
- **Database Design**: PostgreSQL schema for races, horses, results
- **Feature Engineering**: Extract meaningful patterns from historical data
- **ML Models**: Random Forest, XGBoost, ensemble methods
- **Betting Strategies**: Value betting, Kelly criterion, combination optimization
- **Backtesting**: Validate strategies on historical data

## Features

### Current Features (v0.1)
- Fetch V75 race calendars
- Retrieve detailed game data
- Access horse, driver, and trainer information
- Resolve horse nationality from multiple sources
- Display formatted race cards

### Planned Features

#### Data Collection
- [x] ATG API client
- [ ] Web scraping fallback
- [ ] Browser automation (Playwright)
- [ ] Alternative data sources (Travsport, Kanal75)
- [ ] Automated daily/weekly collection
- [ ] Historical data backfill

#### Data Storage
- [ ] PostgreSQL database
- [ ] SQLAlchemy ORM models
- [ ] Data validation and cleaning
- [ ] Caching with Redis
- [ ] Database migrations with Alembic

#### Analysis
- [ ] Feature engineering pipeline
- [ ] Statistical analysis tools
- [ ] Form analysis
- [ ] Track and distance analysis
- [ ] Driver/trainer statistics
- [ ] Pace analysis

#### Machine Learning
- [ ] Training data preparation
- [ ] Multiple model types (RF, XGBoost, LightGBM)
- [ ] Model ensemble
- [ ] Hyperparameter optimization
- [ ] Model evaluation and validation
- [ ] Feature importance analysis

#### Betting Strategy
- [ ] Value betting system
- [ ] Kelly criterion staking
- [ ] Combination optimizer for V75
- [ ] Bankroll management
- [ ] Risk controls
- [ ] Multiple betting systems

#### Backtesting
- [ ] Historical performance testing
- [ ] Performance metrics (ROI, Sharpe, drawdown)
- [ ] Strategy comparison
- [ ] Monte Carlo simulation
- [ ] Walk-forward analysis

#### Interface
- [ ] FastAPI REST API
- [ ] Command-line interface
- [ ] Web dashboard (optional)
- [ ] Automated reports
- [ ] Alerts and notifications

## Project Structure

```
v75/
├── v75.py                      # Current implementation
├── describe_json.py            # JSON analysis utility
├── atgOpenAPI.yaml            # API specification
├── explore_api.py             # API endpoint discovery
│
├── docs/                      # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── ARCHITECTURE_PROPOSAL.md
│   └── IMPLEMENTATION_GUIDE.md
│
├── tests/                     # Test suite
│   └── test_v75_dates.py
│
└── README.md                  # This file
```

### Proposed Structure

See [ARCHITECTURE_PROPOSAL.md](ARCHITECTURE_PROPOSAL.md) for detailed project structure.

## Technology Stack

### Current
- Python 3.x
- Requests (HTTP client)
- Custom SSL adapter for ATG API

### Proposed

| Layer | Technologies |
|-------|-------------|
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL, Redis |
| **Web Framework** | FastAPI, Uvicorn |
| **ORM** | SQLAlchemy, Alembic |
| **ML** | scikit-learn, XGBoost, LightGBM |
| **Data** | pandas, numpy, scipy |
| **Scraping** | BeautifulSoup4, Selenium, Playwright |
| **Tasks** | Celery, Flower |
| **Testing** | pytest, pytest-cov |
| **Deployment** | Docker, Docker Compose |

## Data Sources

### Primary
1. **ATG API** (currently unavailable)
   - Racing calendar
   - Game details
   - Horse information
   - Results

### Alternative Sources
1. **Web Scraping**
   - ATG.se website
   - Travsport.se (official)
   - Kanal75.se (statistics)

2. **Third-Party APIs**
   - Svensk Travsport API (requires partnership)
   - International racing APIs

## Getting Started with Development

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Git

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd v75

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb v75_db

# Run tests
pytest

# Start development server (future)
uvicorn src.api.main:app --reload
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_v75_dates.py
```

## API Examples

### Current API Usage

```python
from v75 import fetch_race_day_data, fetch_v75_game_data

# Get race calendar
data = fetch_race_day_data("2024-10-12")

# Get game details
game_data = fetch_v75_game_data("V75_2024-10-12_32_5")
```

### Future API Usage

```python
from src.data_collection import RaceDataCollector
from src.analysis.models import RacePredictor
from src.strategy.systems import ValueBettingStrategy

# Collect data
collector = RaceDataCollector()
races = await collector.collect_race_day("2024-10-12")

# Make predictions
predictor = RacePredictor()
predictions = predictor.predict_race(race_starts)

# Generate betting system
strategy = ValueBettingStrategy()
system = strategy.generate_v75_system(predictions, budget=500)
```

## Contributing

This is a research/educational project. Contributions are welcome!

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request

### Coding Standards
- PEP 8 style guide
- Type hints
- Docstrings for all functions
- Unit tests for new features

## Legal & Ethical Considerations

### Important Notices

⚠️ **Legal Disclaimer**
- This project is for educational and research purposes only
- Check ATG's Terms of Service before using
- Respect rate limits and robots.txt
- Commercial use may require licensing
- All data rights belong to ATG

⚠️ **Responsible Gambling**
- Never bet more than you can afford to lose
- Past performance doesn't guarantee future results
- Be aware of gambling addiction risks
- This is not financial advice
- For entertainment/research only

### Recommended Practices
1. Start with paper trading (no real money)
2. Use strict bankroll limits
3. Track all bets and performance
4. Stop if showing signs of problem gambling
5. Seek help if needed: [Stödlinjen](https://www.stodlinjen.se/) 020-81 91 00

## Performance Goals

### Model Performance
- Win prediction accuracy > 35%
- Top-3 prediction accuracy > 70%
- Calibration error < 5%

### Betting Performance (Backtested)
- Positive ROI over 100+ games
- Sharpe ratio > 1.0
- Max drawdown < 30%
- Win rate > 40%

### System Performance
- Data collection success > 95%
- API response time < 500ms
- System uptime > 99.5%

## Resources

### Swedish Horse Racing
- [ATG](https://www.atg.se) - Official betting operator
- [Svensk Travsport](https://travsport.se) - Official organization
- [Kanal75](https://www.kanal75.se) - V75 analysis and statistics

### Machine Learning
- [scikit-learn Documentation](https://scikit-learn.org)
- [XGBoost Guide](https://xgboost.readthedocs.io)
- [Kaggle Feature Engineering](https://www.kaggle.com/learn/feature-engineering)

### Betting Strategy
- [Kelly Criterion](https://en.wikipedia.org/wiki/Kelly_criterion)
- [Value Betting Guide](https://www.pinnacle.com/en/betting-articles/Betting-Strategy/what-is-value-betting)
- [Bankroll Management](https://www.sportsbettingdime.com/guides/strategy/bankroll-management/)

## License

This project is for educational purposes. Please ensure compliance with local laws and ATG's terms of service.

## Contact & Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Review documentation in `/docs`
- Check implementation guide for help

## Changelog

### v0.2 (Planned)
- Multi-source data collection
- PostgreSQL database
- Basic feature engineering
- Initial ML models

### v0.1 (Current)
- ATG API client
- Race data display
- Basic documentation
- Test suite

## Acknowledgments

- ATG for providing Swedish horse racing
- Swedish trotting community
- Open source ML community

---

**Remember**: This is a research project. Always gamble responsibly and within your means. The goal is to learn about data analysis and machine learning, not to guarantee profits.
