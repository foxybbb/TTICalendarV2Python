#!/usr/bin/env python3
"""
TSI Calendar Scraper
Fetches calendar data from TSI mob-back portal
"""

import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import config


class TSICalendar:
    """TSI Calendar scraper class"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"
        })
        self.events = []
    
    def login(self):
        """Authenticate with TSI portal"""
        # Get login page and extract CSRF token
        resp = self.session.get(config.LOGIN_PAGE)
        soup = BeautifulSoup(resp.text, "html.parser")
        token_input = soup.find("input", attrs={"name": "_token"})
        
        if not token_input or not token_input.get("value"):
            raise RuntimeError("Could not find CSRF token")
        
        csrf_token = token_input["value"]
        
        # Login with multipart/form-data
        login_data = {
            "_token": (None, csrf_token),
            "username": (None, config.USERNAME),
            "password": (None, config.PASSWORD),
        }
        
        headers = {
            "Referer": config.LOGIN_PAGE,
            "Origin": config.BASE_URL,
        }
        
        resp = self.session.post(config.AUTH_URL, files=login_data, headers=headers, allow_redirects=True)
        
        # Check if login was successful
        if "logout" not in resp.text.lower():
            raise RuntimeError("Login failed - check credentials")
        
        print("Login successful")
    
    def fetch_month(self, year, month):
        """Fetch calendar data for a specific month"""
        params = {
            "view": "month",
            "date": f"{year}-{month:02d}-01",
            "room": config.FILTERS["room"],
            "lecturer": config.FILTERS["lecturer"],
            "group": config.FILTERS["group"],
            "type[]": config.FILTERS["type"],
            "year": year,
            "month": month
        }
        
        resp = self.session.get(config.CALENDAR_URL, params=params)
        resp.raise_for_status()
        
        return self._parse_events(resp.text)
    
    def _parse_events(self, html):
        """Parse events from calendar HTML"""
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")
        
        for script in scripts:
            if script.string and "const events" in script.string:
                # Extract JSON with events
                match = re.search(r'const events = (\{[^;]+\});', script.string, re.DOTALL)
                if match:
                    try:
                        events_by_date = json.loads(match.group(1))
                        events = []
                        for date, date_events in events_by_date.items():
                            for event in date_events:
                                event['date'] = date
                                events.append(event)
                        return events
                    except json.JSONDecodeError as e:
                        print(f"Warning: JSON parse error - {e}")
        
        return []
    
    def fetch_period(self, from_year, from_month, to_year, to_month):
        """Fetch calendar data for a period"""
        all_events = []
        current_date = datetime(from_year, from_month, 1)
        end_date = datetime(to_year, to_month, 1)
        
        while current_date <= end_date:
            print(f"Fetching {current_date.strftime('%B %Y')}...", end=" ")
            events = self.fetch_month(current_date.year, current_date.month)
            print(f"Found {len(events)} events")
            all_events.extend(events)
            current_date = current_date + relativedelta(months=1)
        
        self.events = all_events
        return all_events
    
    def get_events(self):
        """Get all fetched events"""
        return self.events
    
    def close(self):
        """Close session"""
        self.session.close()


def sort_events(events, sort_by="date"):
    """Sort events by specified field"""
    sort_keys = {
        "date": lambda e: (e.get('date', ''), e.get('start_time', '')),
        "room": lambda e: (e.get('room', ''), e.get('date', ''), e.get('start_time', '')),
        "lecturer": lambda e: (e.get('lecturer', ''), e.get('date', ''), e.get('start_time', '')),
        "group": lambda e: (e.get('group', ''), e.get('date', ''), e.get('start_time', '')),
        "time": lambda e: (e.get('start_time', ''), e.get('date', ''))
    }
    
    return sorted(events, key=sort_keys.get(sort_by, sort_keys["date"]))


def filter_events(events):
    """Filter events based on display options"""
    if not config.DISPLAY["show_canceled"]:
        events = [e for e in events if e.get('description', '').lower() != 'canceled']
    return events

