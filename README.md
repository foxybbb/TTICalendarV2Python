# TSI Calendar Scraper v2

A Python application to scrape calendar events from the Transport and Telecommunication Institute (TSI) portal and export them to various formats.

## Features

- **Authentication**: Secure login to TSI mob-back portal
- **Flexible Filtering**: Filter by room, lecturer, group, and event type
- **Date Range Support**: Fetch events for multiple months
- **Multiple Export Formats**:
  - **Table**: Display events in formatted table in terminal
  - **JSON**: Export to JSON file for further processing
  - **ICS**: Export to iCalendar format (compatible with Google Calendar, Outlook, Apple Calendar)
  - **Google Calendar**: Direct export to Google Calendar (requires API setup)
- **Sorting Options**: Sort by date, room, lecturer, group, or time
- **Filter Canceled Events**: Option to show or hide canceled events
- **DST Support**: Automatic handling of Daylight Saving Time transitions (winter/summer time) for accurate calendar times

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your credentials in `config.py`:
```python
USERNAME = "your_username"
PASSWORD = "your_password"
```

## Configuration

Edit `config.py` to customize:

### Filters
```python
FILTERS = {
    "room": "reset_room",        # Specific room or "reset_room" for all
    "lecturer": "Gercevs",       # Lecturer name or "reset_lecturer" for all
    "group": "3903BDA",          # Group code or "reset_group" for all
    "type": "reset_type"         # Event type or "reset_type" for all
}
```

### Date Range
```python
DATE_RANGE = {
    "from_year": 2025,
    "from_month": 9,     # September
    "to_year": 2025,
    "to_month": 12       # December
}
```

### Display Options
```python
DISPLAY = {
    "sort_by": "date",         # Options: "date", "room", "lecturer", "group", "time"
    "show_canceled": True      # Show or hide canceled events
}
```

### Output Formats
```python
OUTPUT = {
    "formats": ["table", "json", "ics"],  # Choose which formats to export
    "json_file": "calendar_events.json",
    "ics_file": "calendar_events.ics",
}
```

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Authenticate with TSI portal
2. Fetch calendar data for the specified period
3. Filter and sort events
4. Export to the specified formats

## Output Formats

### Table Output
Displays events in a formatted table in the terminal:
```
Date         | Time          | Title                      | Room       | Group    | Lecturer  | Type   | Note
2025-11-01 S | 08:45-10:15   | Electronics...             | L8 (125)   | 3401BNA  | Gercevs   | Lesson | -
```

### JSON Output
Exports events to a JSON file:
```json
[
  {
    "date": "2025-11-01",
    "start_time": "08:45",
    "end_time": "10:15",
    "title": "Electronics and Microelectronics",
    "room": "L8 (125)",
    "group": "3401BNA, 3403BNA",
    "lecturer": "Gercevs Ivans",
    "type": "Lesson",
    "description": ""
  }
]
```

### ICS Output
Creates an iCalendar file compatible with:
- Google Calendar
- Microsoft Outlook
- Apple Calendar
- Other calendar applications

Import by:
1. Opening your calendar application
2. Selecting "Import Calendar"
3. Choosing the `calendar_events.ics` file

### Google Calendar Export

To use Google Calendar direct export:

1. Enable Google Calendar API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json`

2. Configure in `config.py`:
```python
GOOGLE_CALENDAR = {
    "calendar_id": "your_calendar_id@group.calendar.google.com",
    "credentials_file": "credentials.json",
    "token_file": "token.json",
    "timezone": "Europe/Riga",
    "location": "Transport and Telecommunication Institute, Lauvas iela 2, Riga, LV-1019, Latvia"
}
```

3. Add `"google_calendar"` to output formats:
```python
OUTPUT = {
    "formats": ["table", "json", "ics", "google_calendar"],
}
```

## Examples

### Example 1: Get all events for a lecturer
```python
FILTERS = {
    "room": "reset_room",
    "lecturer": "Gercevs",
    "group": "reset_group",
    "type": "reset_type"
}
```

### Example 2: Get events for a specific group
```python
FILTERS = {
    "room": "reset_room",
    "lecturer": "reset_lecturer",
    "group": "5502DTL",
    "type": "reset_type"
}
```

### Example 3: Get events in a specific room
```python
FILTERS = {
    "room": "L1 (125)",
    "lecturer": "reset_lecturer",
    "group": "reset_group",
    "type": "reset_type"
}
```

### Example 4: Sort by room
```python
DISPLAY = {
    "sort_by": "room",
    "show_canceled": False  # Hide canceled events
}
```

## Project Structure

```
TTICalendarV2Python/
├── config.py           # Configuration file
├── main.py            # Main entry point
├── TSICalendar.py     # Calendar scraper
├── Exporters.py       # Export to various formats
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## Timezone and DST Handling

The application properly handles Daylight Saving Time (DST) transitions:

- **Automatic DST Detection**: Uses `pytz` library to automatically detect whether DST is active for each event date
- **Europe/Riga Timezone**: Configured for TSI location (GMT+2 in winter, GMT+3 in summer)
- **Accurate Times**: Events exported to Google Calendar and ICS files will have correct local times regardless of DST
- **No Manual Adjustments**: No need to manually adjust times for winter/summer transitions

### How It Works

The application uses timezone-aware datetime objects:
```python
# Before (naive datetime - incorrect DST handling):
datetime(2025, 11, 15, 10, 30)  # Ambiguous - is this winter or summer time?

# After (timezone-aware - correct DST handling):
timezone.localize(datetime(2025, 11, 15, 10, 30))  # Automatically uses EET (winter)
timezone.localize(datetime(2025, 9, 15, 10, 30))   # Automatically uses EEST (summer)
```

This ensures that:
- Events in **summer** (March-October) are correctly marked as EEST (UTC+3)
- Events in **winter** (November-March) are correctly marked as EET (UTC+2)
- Calendar applications will display the correct local time

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- python-dateutil
- pytz (for proper DST handling)

Optional (for ICS export):
- ics

Optional (for Google Calendar):
- google-auth
- google-auth-oauthlib
- google-api-python-client

## License

This project is for educational purposes.

## Support

For issues or questions, please check your configuration and ensure:
- Credentials are correct
- Date range is valid
- Required packages are installed
- Network connection is available
