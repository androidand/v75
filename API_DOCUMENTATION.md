# ATG Racing Information API Documentation

## Overview

This document provides comprehensive documentation for the ATG (Swedish Horse Racing) Racing Information API, reverse-engineered from publicly available sources.

**Base URL:** `https://www.atg.se/services/racinginfo/v1/api`

**Note:** As of October 2025, the API appears to have implemented stricter access controls (403 Forbidden responses). This may require:
- Authentication tokens
- Specific request headers
- IP whitelisting
- Access from Swedish IP addresses only

## Current Status

### Working Endpoints (Historical)

The following endpoints were functional as of the initial codebase implementation:

#### 1. Calendar Day Endpoint
```
GET /calendar/day/{date}
```

**Parameters:**
- `date` (string, required): Date in format YYYY-MM-DD

**Response Structure:**
```json
{
  "date": "2024-10-05",
  "tracks": [
    {
      "id": 32,
      "name": "Solvalla",
      "biggestGameType": "V75",
      "races": [
        {
          "id": "2024-10-05_32_1",
          "startTime": "2024-10-05T18:20:00",
          "number": 1
        }
      ]
    }
  ],
  "games": {
    "V75": [
      {
        "id": "V75_2024-10-05_32_5",
        "races": ["2024-10-05_32_1", "2024-10-05_32_2", ...]
      }
    ]
  }
}
```

**Use Cases:**
- Find V75 game days
- Get track information
- Retrieve race schedules
- Identify game IDs for detailed queries

#### 2. Game Detail Endpoint
```
GET /games/{game_id}
```

**Parameters:**
- `game_id` (string, required): Game identifier (e.g., "V75_2024-10-05_32_5")

**Response Structure:**
```json
{
  "id": "V75_2024-10-05_32_5",
  "status": "results",
  "races": [
    {
      "id": "2024-10-05_32_1",
      "number": 1,
      "name": "Race Name",
      "scheduledStartTime": "2024-10-05T18:20:00",
      "startTime": "2024-10-05T18:20:15",
      "distance": 2140,
      "startMethod": "auto|volt",
      "starts": [
        {
          "number": 1,
          "horse": {
            "id": 789012,
            "name": "Horse Name",
            "nationality": "SE",
            "money": 1234567,
            "pedigree": {
              "father": {
                "name": "Father Name",
                "nationality": "US"
              },
              "mother": {
                "name": "Mother Name",
                "nationality": "SE"
              },
              "grandfather": {
                "name": "Grandfather Name",
                "nationality": "FR"
              }
            }
          },
          "driver": {
            "firstName": "John",
            "lastName": "Doe"
          },
          "trainer": {
            "firstName": "Jane",
            "lastName": "Smith"
          }
        }
      ]
    }
  ]
}
```

**Use Cases:**
- Get complete race card
- Access horse, driver, and trainer information
- Retrieve pedigree data
- Access race distance and start method

#### 3. Horse Detail Endpoint
```
GET /horses/{horse_id}
```

**Parameters:**
- `horse_id` (integer, required): Horse identifier

**Response Structure:**
```json
{
  "id": 789012,
  "name": "Horse Name",
  "age": 5,
  "sex": "gelding|mare|stallion",
  "nationality": "SE",
  "money": 1234567,
  "pedigree": {
    "father": {
      "id": 123456,
      "name": "Father Name",
      "nationality": "US"
    },
    "mother": {
      "id": 234567,
      "name": "Mother Name",
      "nationality": "SE"
    },
    "grandfather": {
      "id": 345678,
      "name": "Grandfather Name",
      "nationality": "FR"
    }
  }
}
```

**Use Cases:**
- Get detailed horse information
- Access complete pedigree
- Retrieve earnings history

## Discovered Endpoints (Not Yet Verified)

Based on research and similar API patterns, the following endpoints may exist:

### Race Endpoints
```
GET /races/{race_id}                    # Detailed race information
GET /races/{race_id}/start              # Race start data
GET /races/{race_id}/pools              # Betting pools for race
GET /races/{race_id}/result             # Race results
```

### Track Endpoints
```
GET /tracks                             # List all tracks
GET /tracks/{track_id}                  # Track details
GET /tracks/{track_id}/program/{date}   # Track program for date
GET /tracks/{track_id}/program/{date}/pdf  # Program PDF
```

### Calendar Endpoints
```
GET /calendar/week/{date}               # Week calendar
GET /calendar/month/{year-month}        # Month calendar
```

### Results Endpoints
```
GET /results/day/{date}                 # Results for a day
GET /results/{game_type}                # Results for game type
```

### Statistics Endpoints
```
GET /drivers                            # List of drivers
GET /drivers/{driver_id}                # Driver details
GET /trainers                           # List of trainers
GET /trainers/{trainer_id}              # Trainer details
```

### Betting Endpoints
```
GET /odds                               # Current odds
GET /pools                              # Betting pools
GET /products                           # Betting products
```

### Live Data Endpoints
```
GET /live                               # Live racing data
GET /live/races                         # Current live races
```

## Data Models

### Race
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique race identifier (format: YYYY-MM-DD_track_number) |
| number | integer | Race number (1-7 for V75) |
| name | string | Race name |
| scheduledStartTime | string (ISO 8601) | Planned start time |
| startTime | string (ISO 8601) | Actual start time |
| distance | integer | Race distance in meters |
| startMethod | string | "auto" (car start) or "volt" (standing start) |
| starts | array | Array of race participants |

### Horse Start
| Field | Type | Description |
|-------|------|-------------|
| number | integer | Starting position |
| horse | object | Horse information |
| driver | object | Driver information |
| trainer | object | Trainer information |

### Horse
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique horse identifier |
| name | string | Horse name |
| nationality | string | Two-letter country code |
| money | integer | Career earnings in SEK |
| age | integer | Horse age in years |
| sex | string | "gelding", "mare", or "stallion" |
| pedigree | object | Pedigree information |

### Person (Driver/Trainer)
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| firstName | string | First name |
| lastName | string | Last name |

### Track
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique track identifier |
| name | string | Track name (e.g., "Solvalla", "Jägersro") |
| biggestGameType | string | Main game type at track |

## Game Types

| Type | Description | Races | Days |
|------|-------------|-------|------|
| V75 | Main weekly pool | 7 | Saturday |
| V86 | Medium pool | 8 | Wednesday & Sunday |
| V64 | Standard pool | 6 | Various |
| V65 | Standard pool | 6 | Various |
| GS75 | Grand Slam 75 | 7 | Special occasions |

## Authentication & Access

### Current Situation (October 2025)
- API returns 403 Forbidden for most requests
- May require authentication token
- Could be geo-restricted to Swedish IPs
- May need specific headers or cookies

### Historical Access
The API was previously accessible without authentication using:
- SSL/TLS with SECLEVEL=1 cipher configuration
- Standard HTTP GET requests
- No special headers required

### Potential Solutions
1. **Browser Automation**: Use Selenium/Playwright to access via browser
2. **Proxy Services**: Route through Swedish proxy
3. **Official Partnership**: Contact ATG for API access
4. **Web Scraping**: Extract data from ATG website directly
5. **Alternative Data Sources**:
   - travsport.se
   - kanal75.se
   - Third-party horse racing data providers

## Rate Limiting

Unknown - API access currently restricted.

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 403 | Forbidden | Access denied (current state) |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |

## Best Practices

1. **Respect Rate Limits**: Don't hammer the API
2. **Cache Responses**: Store results locally to minimize requests
3. **Handle Errors Gracefully**: Always check status codes
4. **Use Proper SSL**: Configure SSL adapter for compatibility
5. **Validate Data**: Check for missing/null values
6. **Monitor Changes**: API structure may change without notice

## Legal Considerations

⚠️ **Important Legal Notice:**

1. **Terms of Service**: Check ATG's terms before using this API
2. **Commercial Use**: May require licensing for commercial applications
3. **Data Rights**: ATG owns all racing data
4. **Responsible Gambling**: Don't encourage problematic gambling behavior
5. **Personal Use**: This documentation is for educational purposes

## Alternative Data Sources

If the API remains inaccessible, consider:

1. **Travsport.se**: Official Swedish trotting website
2. **Svensk Travsport API**: Official industry API (requires partnership)
3. **Kanal75**: V75 analysis and statistics
4. **The Racing API**: Third-party international racing data
5. **Web Scraping**: Extract from public ATG web pages (check ToS)

## Example Code

See `v75.py` for complete implementation examples.

### Basic Request Pattern
```python
import requests
from requests.adapters import HTTPAdapter
import ssl

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT:@SECLEVEL=1")
        kwargs["ssl_context"] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount("https://", SSLAdapter())
response = session.get("https://www.atg.se/services/racinginfo/v1/api/calendar/day/2024-10-05")
```

## Changelog

- **2025-10-21**: Documented API access restrictions (403 errors)
- **2024-10**: Initial API exploration and documentation
- **Earlier**: API was publicly accessible without authentication
