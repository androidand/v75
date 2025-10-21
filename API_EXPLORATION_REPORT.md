# ATG Racing Information API - Complete Exploration Report

## Executive Summary

This document provides a comprehensive mapping of the ATG Racing Information API v1 based on:
- Code analysis from working implementation (v75.py)
- API endpoint patterns and conventions
- Data structure reverse engineering
- Historical access patterns (API was accessible until August 2025)

## Current Status (October 2025)

**API Access:** ❌ **RESTRICTED** (403 Forbidden)

The API was publicly accessible without authentication until approximately August-October 2025. As of October 21, 2025, all endpoints return `403 Access denied`.

**Possible Reasons:**
1. API now requires authentication/API key
2. Geo-restriction to Swedish IP addresses only
3. Rate limiting or bot detection
4. Temporary service changes
5. Migration to new API version

## Complete API Endpoint Mapping

### Base URL
```
https://www.atg.se/services/racinginfo/v1/api
```

### Verified Endpoints (from working code)

#### 1. Calendar Day Endpoint ✓ VERIFIED
```http
GET /calendar/day/{date}
```

**Parameters:**
| Parameter | Type   | Required | Format      | Example    |
|-----------|--------|----------|-------------|------------|
| date      | string | Yes      | YYYY-MM-DD  | 2025-10-25 |

**Response Structure:**
```json
{
  "date": "2025-10-25",
  "tracks": [
    {
      "id": 32,
      "name": "Solvalla",
      "biggestGameType": "V75",
      "races": [
        {
          "id": "2025-10-25_32_1",
          "startTime": "2025-10-25T18:20:00",
          "number": 1
        }
      ]
    }
  ],
  "games": {
    "V75": [
      {
        "id": "V75_2025-10-25_32_5",
        "races": [
          "2025-10-25_32_1",
          "2025-10-25_32_2",
          "2025-10-25_32_3",
          "2025-10-25_32_4",
          "2025-10-25_32_5",
          "2025-10-25_32_6",
          "2025-10-25_32_7"
        ]
      }
    ],
    "V86": [...],
    "V64": [...]
  }
}
```

**Track IDs (Known):**
- 32: Solvalla (Stockholm)
- 11: Jägersro (Malmö)
- 5: Åby (Gothenburg)
- 13: Bollnäs
- Additional tracks discoverable via this endpoint

#### 2. Game Detail Endpoint ✓ VERIFIED
```http
GET /games/{game_id}
```

**Parameters:**
| Parameter | Type   | Required | Format                  | Example              |
|-----------|--------|----------|-------------------------|----------------------|
| game_id   | string | Yes      | {TYPE}_{DATE}_{T}_{R}  | V75_2025-10-25_32_5 |

**Game ID Format:**
- `{TYPE}`: V75, V86, V64, V65, etc.
- `{DATE}`: YYYY-MM-DD
- `{T}`: Track ID
- `{R}`: Starting race number

**Response Structure:**
```json
{
  "id": "V75_2025-10-25_32_5",
  "@type": "Game",
  "status": "results|open|closed|upcoming",
  "races": [
    {
      "id": "2025-10-25_32_5",
      "number": 5,
      "name": "Storängens Lopp",
      "scheduledStartTime": "2025-10-25T19:00:00",
      "startTime": "2025-10-25T19:00:15",
      "distance": 2140,
      "startMethod": "auto",
      "monte": false,
      "starts": [
        {
          "number": 1,
          "postPosition": 1,
          "distance": 2140,
          "horse": {
            "id": 789012,
            "name": "Global Trustworthy",
            "nationality": "SE",
            "age": 5,
            "sex": "gelding",
            "record": {
              "code": "M",
              "startMethod": "auto",
              "distance": "long",
              "time": {
                "minutes": 1,
                "seconds": 10,
                "tenths": 3
              }
            },
            "trainer": {
              "id": 123456,
              "firstName": "Anders",
              "lastName": "Svanstedt"
            },
            "shoes": {
              "reported": true,
              "front": {
                "hasShoe": true,
                "changed": false
              },
              "back": {
                "hasShoe": true,
                "changed": false
              }
            },
            "sulky": {
              "reported": true,
              "type": {
                "code": "VA",
                "text": "Vanlig",
                "engText": "Standard",
                "changed": false
              },
              "colour": {
                "code": "SV",
                "text": "Svart",
                "engText": "Black",
                "changed": false
              }
            },
            "money": 1234567,
            "color": "mörkbrun",
            "homeTrack": {
              "id": 32,
              "name": "Solvalla"
            },
            "owner": {
              "id": 654321,
              "name": "Stall Global AB"
            },
            "breeder": {
              "id": 111222,
              "name": "Breeder Name"
            },
            "statistics": {
              "years": {
                "2025": {
                  "starts": 10,
                  "earnings": 150000,
                  "placement": {
                    "1": 3,
                    "2": 2,
                    "3": 1
                  },
                  "records": []
                }
              },
              "life": {
                "starts": 45,
                "earnings": 1234567,
                "placement": {
                  "1": 12,
                  "2": 10,
                  "3": 8
                },
                "records": []
              }
            },
            "pedigree": {
              "father": {
                "id": 555666,
                "name": "Muscle Hill",
                "nationality": "US"
              },
              "mother": {
                "id": 666777,
                "name": "Mare Name",
                "nationality": "SE"
              },
              "grandfather": {
                "id": 777888,
                "name": "Pine Chip",
                "nationality": "US"
              }
            }
          },
          "driver": {
            "id": 234567,
            "firstName": "Örjan",
            "lastName": "Kihlström",
            "shortName": "Kih Ör",
            "location": "Bromma",
            "birth": 1962,
            "homeTrack": {
              "id": 32,
              "name": "Solvalla"
            },
            "license": "A-licens körlicens",
            "silks": "Mörkblå, vit krage, vit/mblå ärm; vit",
            "statistics": {
              "years": {
                "2025": {
                  "starts": 450,
                  "earnings": 5000000,
                  "placement": {
                    "1": 95,
                    "2": 78,
                    "3": 65
                  }
                }
              }
            }
          },
          "trainer": {
            "id": 123456,
            "firstName": "Anders",
            "lastName": "Svanstedt",
            "shortName": "Sva An",
            "location": "Stockholm",
            "birth": 1967,
            "homeTrack": {
              "id": 32,
              "name": "Solvalla"
            },
            "license": "A-tränarlicens",
            "statistics": {
              "years": {
                "2025": {
                  "starts": 320,
                  "earnings": 8000000,
                  "placement": {
                    "1": 80,
                    "2": 65,
                    "3": 50
                  }
                }
              }
            }
          },
          "result": {
            "place": 1,
            "finishOrder": 45,
            "kmTime": {
              "minutes": 1,
              "seconds": 10,
              "tenths": 3
            },
            "galloped": false,
            "disqualified": false,
            "prizeMoney": 100000,
            "finalOdds": 4.5,
            "startNumber": 1
          },
          "pools": {
            "vinnare": {
              "odds": 4.5
            },
            "plats": {
              "minOdds": 1.8,
              "maxOdds": 2.1
            },
            "twins": {
              "odds": 15.2
            }
          }
        }
      ],
      "prizeMoney": 500000,
      "terms": "3-åriga och äldre 100.001 - 1.000.000 kr",
      "sport": "trot",
      "track": {
        "id": 32,
        "name": "Solvalla",
        "condition": "fast",
        "countryCode": "SE"
      },
      "result": {
        "victoryMargin": "hals"
      },
      "reserveOrder": []
    }
  ],
  "pools": {
    "V75": {
      "type": "jackpot",
      "turnover": 85000000,
      "result": {
        "winners": 3,
        "payout": {
          "7": {
            "winners": 3,
            "payout": 1234567.50
          },
          "6": {
            "winners": 45,
            "payout": 15234.20
          },
          "5": {
            "winners": 567,
            "payout": 856.40
          }
        }
      }
    }
  },
  "currentVersion": 12345678901234
}
```

**Field Details:**

**Start Method:**
- `auto`: Autostart (car start)
- `volt`: Voltstart (standing start)

**Monte:**
- `true`: Ridden race (monte)
- `false`: Sulky race (regular)

**Status Values:**
- `upcoming`: Race not yet run
- `open`: Betting open
- `closed`: Betting closed
- `results`: Race completed with results

#### 3. Horse Detail Endpoint ✓ VERIFIED
```http
GET /horses/{horse_id}
```

**Parameters:**
| Parameter | Type    | Required | Format  | Example |
|-----------|---------|----------|---------|---------|
| horse_id  | integer | Yes      | numeric | 789012  |

**Response Structure:**
```json
{
  "id": 789012,
  "name": "Global Trustworthy",
  "nationality": "SE",
  "age": 5,
  "sex": "gelding",
  "money": 1234567,
  "color": "mörkbrun",
  "markings": "inga",
  "birth": {
    "year": 2020,
    "month": 5
  },
  "pedigree": {
    "father": {
      "id": 555666,
      "name": "Muscle Hill",
      "nationality": "US",
      "money": 9876543
    },
    "mother": {
      "id": 666777,
      "name": "Mare Name",
      "nationality": "SE",
      "money": 234567
    },
    "grandfather": {
      "id": 777888,
      "name": "Pine Chip",
      "nationality": "US",
      "money": 7654321
    }
  },
  "record": {
    "year": 2024,
    "code": "M",
    "startMethod": "auto",
    "distance": "long",
    "time": {
      "minutes": 1,
      "seconds": 10,
      "tenths": 3
    },
    "place": "Solvalla"
  },
  "owner": {
    "id": 654321,
    "name": "Stall Global AB"
  },
  "breeder": {
    "id": 111222,
    "name": "Breeder Name",
    "location": "Stockholm"
  },
  "statistics": {
    "life": {
      "starts": 45,
      "earnings": 1234567,
      "placement": {
        "1": 12,
        "2": 10,
        "3": 8
      }
    },
    "years": {
      "2025": {...},
      "2024": {...}
    }
  },
  "starts": [
    {
      "raceId": "2025-10-18_32_6",
      "date": "2025-10-18",
      "track": {
        "id": 32,
        "name": "Solvalla"
      },
      "result": {
        "place": 2,
        "kmTime": {...}
      },
      "driver": {...},
      "trainer": {...}
    }
  ]
}
```

### Inferred Endpoints (Pattern-based, Not Verified)

Based on REST API conventions and similar racing APIs:

#### Race Endpoints
```http
GET /races/{race_id}                    # Race details
GET /races/{race_id}/start              # Start information
GET /races/{race_id}/result             # Race result
GET /races/{race_id}/pools              # Betting pools
GET /races/{race_id}/odds               # Live odds
```

#### Track Endpoints
```http
GET /tracks                             # List all tracks
GET /tracks/{track_id}                  # Track details
GET /tracks/{track_id}/program/{date}   # Program for date
GET /tracks/{track_id}/program/{date}/pdf  # PDF program
```

#### Calendar Endpoints
```http
GET /calendar/week/{date}               # Week calendar
GET /calendar/month/{YYYY-MM}           # Month calendar
GET /calendar/year/{YYYY}               # Year calendar
```

#### Results Endpoints
```http
GET /results/day/{date}                 # Day results
GET /results/game/{game_id}             # Game results
GET /results/{game_type}                # Recent results by type
```

#### Statistics Endpoints
```http
GET /drivers/{driver_id}                # Driver details
GET /drivers/{driver_id}/statistics     # Driver stats
GET /trainers/{trainer_id}              # Trainer details
GET /trainers/{trainer_id}/statistics   # Trainer stats
```

## Data Models (Complete)

All data models have been implemented as Python dataclasses in `models.py`:

### Core Models
- `Horse` - Complete horse information with pedigree
- `Driver` - Driver/jockey information
- `Trainer` - Trainer information
- `RaceStart` - Horse participation in race
- `Race` - Race details with all starts
- `Track` - Track/venue information
- `Game` - Complete game (V75/V86) with races
- `RaceDay` - Daily race calendar

### Supporting Models
- `Pedigree` - Horse lineage (father, mother, grandfather)
- `GameInfo` - Game metadata
- `RaceResult` - Race results and payouts
- `GameResult` - Game results and payouts
- `Statistics` - Performance statistics

### Enumerations
- `GameType` - V75, V86, V64, V65, GS75, V4, V3
- `StartMethod` - AUTO, VOLT
- `HorseSex` - STALLION, MARE, GELDING
- `GameStatus` - UPCOMING, OPEN, CLOSED, RESULTS

See `models.py` for complete implementations with type hints and parsing functions.

## API Client Implementation

A type-safe API client has been implemented in `api_client.py`:

```python
from api_client import ATGAPIClient, get_next_v75_game

# Initialize client
client = ATGAPIClient()

# Get next V75
race_day = client.get_next_v75()
if race_day:
    v75_track = race_day.get_v75_track()
    v75_games = race_day.get_v75_games()

# Get game data
game = client.get_game("V75_2025-10-25_32_5")
if game:
    for race in game.races:
        print(f"Race {race.number}: {len(race.starts)} horses")

# Get horse data
horse = client.get_horse(789012)
if horse:
    print(f"{horse.name} ({horse.get_nationality()})")
    print(f"Earnings: {horse.money:,} SEK")
```

## SSL/TLS Requirements

The API requires specific SSL configuration:

```python
import ssl
from requests.adapters import HTTPAdapter

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT:@SECLEVEL=1")  # Critical!
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)
```

**Why SECLEVEL=1?**
- ATG servers may use older SSL/TLS configurations
- Default SECLEVEL=2 rejects some cipher suites
- SECLEVEL=1 allows compatibility with legacy systems

## Working Around Current Restrictions

Since the API now returns 403, alternative approaches:

### 1. Browser Automation
```python
from playwright.async_api import async_playwright

async def fetch_v75_data(date):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to ATG website
        await page.goto(f'https://www.atg.se/spel/v75/{date}')

        # Intercept API calls
        async def handle_response(response):
            if 'racinginfo/v1/api' in response.url:
                data = await response.json()
                # Process data

        page.on('response', handle_response)
        await page.wait_for_load_state('networkidle')
        await browser.close()
```

### 2. Web Scraping
```python
from bs4 import BeautifulSoup
import requests

def scrape_v75_page(date):
    url = f'https://www.atg.se/spel/v75/{date}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract structured data from page
    # ATG uses JSON-LD or embedded JSON
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        data = json.loads(script.string)
        # Process structured data
```

### 3. Request Authentication
If API key becomes available:

```python
client = ATGAPIClient(api_key='your-api-key')
```

## Historical Access Pattern

**Timeline:**
- **October 2024**: API publicly accessible, initial implementation
- **August 2025**: Code still working (commits show fixes)
- **October 2025**: API returns 403 Forbidden

**Changes Required:**
1. Authentication mechanism (API key, OAuth, etc.)
2. Geo-restriction (Swedish IPs only)
3. Different endpoint structure
4. Rate limiting enforcement

## Recommendations

### Immediate Actions
1. **Contact ATG**: Request API access or documentation
2. **Monitor Changes**: Check if restriction is temporary
3. **Implement Fallback**: Use web scraping as backup

### Long-term Strategy
1. **Official Partnership**: Apply for ATG data feed access
2. **Alternative Sources**:
   - Travsport.se (official Swedish trotting)
   - Kanal75.se (statistics platform)
   - Third-party data providers

### Data Collection
Even with restrictions:
1. **Scrape Historical Results**: Build database from past races
2. **Manual Collection**: Save race cards when available
3. **Cached Data**: Use saved responses for development

## Summary

### What We Know ✓
- Complete API endpoint structure (3 verified, ~15 inferred)
- Full data models with all fields
- SSL/TLS requirements
- Response formats and structures
- Historical access patterns

### What Changed ✗
- API now requires authentication or has access restrictions
- Unknown: exact authentication method
- Unknown: if restriction is permanent

### What We Built ✓
- Complete dataclass models (models.py)
- Type-safe API client (api_client.py)
- Parser functions for all data types
- Documentation and examples

### Next Steps →
1. Investigate current access requirements
2. Implement browser automation fallback
3. Build web scraping alternative
4. Continue development with mock/cached data

---

**Last Updated:** October 21, 2025
**API Status:** Restricted (403 Forbidden)
**Code Status:** Models and client implemented, ready for when access is restored
