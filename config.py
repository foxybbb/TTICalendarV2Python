# Configuration file for TSI Calendar Scraper

# Authentication
USERNAME = "stXXXXX"
PASSWORD = "XXXXXXXXX"

# Calendar filters
FILTERS = {
    "room": "reset_room",      # Example: "221", "L1 (125)", or "reset_room" for all
    "lecturer": "Gercevs",     # Example: "Gercevs" or "reset_lecturer" for all
    "group": "reset_group",    # Example: "5502DTL", "3401BNA" or "reset_group" for all
    "type": "reset_type"       # Event type filter or "reset_type" for all
}

DATE_RANGE = {
    "from_year": 2025,
    "from_month": 9,    # September
    "to_year": 2025,
    "to_month": 12      # December
}

# Display options
DISPLAY = {
    "sort_by": "date",  # Options: "date", "room", "lecturer", "group", "time"
    "show_canceled": True  
}


OUTPUT = {
    "formats": ["table", "ics"],  # Options: "table", "json", "ics", "google_calendar" for google folow MD file
    "json_file": "calendar_tsi.json",
    "ics_file": "calendar_tsi.ics",
}

# Google Calendar settings (only if using google_calendar output)
GOOGLE_CALENDAR = {
    "calendar_id": "xxxxxxxxxxxxxxxxxxxxxxxxxx@group.calendar.google.com",  # Change to your calendar ID
    "credentials_file": "credentials.json",
    "token_file": "token.json",
    "timezone": "Europe/Riga",
    "location": "Transport and Telecommunication Institute, Lauvas iela 2, Riga, LV-1019, Latvia"
}

# API endpoints
BASE_URL = "https://mob-back.tsi.lv"
LOGIN_PAGE = f"{BASE_URL}/login"
AUTH_URL = f"{BASE_URL}/authenticate"
CALENDAR_URL = f"{BASE_URL}/calendar"

