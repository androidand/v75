# V75 Racing Info Script

This script retrieves and displays V75 race day data, including detailed horse and race information from ATG's API. It can list all V75 game dates for the current year and fetch detailed horse nationality information, including pedigree details when needed.

## Usage

1. **Fetch Data for Next V75 Game Day**:
   ```bash
   python3 v75.py
   ```

2. **Fetch Data for a Specific Date** (`YYYY-MM-DD` format):
   ```bash
   python3 v75.py 2024-10-12
   ```

3. **List All V75 Dates for the Current Year**:
   ```bash
   python3 v75.py list-dates
   ```

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)
