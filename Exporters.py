#!/usr/bin/env python3
"""
Export calendar events to various formats
"""

import json
from datetime import datetime, timedelta
import config

# Optional imports
try:
    from ics import Calendar, Event
    HAS_ICS = True
except ImportError:
    HAS_ICS = False


class TableExporter:
    """Export events in table format"""
    
    @staticmethod
    def export(events):
        """Display events in table format"""
        if not events:
            print("No events to display")
            return
        
        # Column widths
        w = {'date': 12, 'time': 13, 'title': 40, 'room': 10, 'group': 22, 'lecturer': 20, 'type': 12, 'note': 15}
        separator = "-" * 160
        
        # Header
        print("\n" + "=" * 160)
        print(f"{'TSI CALENDAR EVENTS':^160}")
        print(f"Total: {len(events)} events | Filters: Room={config.FILTERS['room']}, "
              f"Lecturer={config.FILTERS['lecturer']}, Group={config.FILTERS['group']}")
        print("=" * 160)
        
        header = (f"{'Date':<{w['date']}} | {'Time':<{w['time']}} | {'Title':<{w['title']}} | "
                  f"{'Room':<{w['room']}} | {'Group':<{w['group']}} | {'Lecturer':<{w['lecturer']}} | "
                  f"{'Type':<{w['type']}} | {'Note':<{w['note']}}")
        print(header)
        print(separator)
        
        # Rows
        for event in events:
            # Parse date
            try:
                date_obj = datetime.strptime(event['date'], "%Y-%m-%d")
                date_str = f"{date_obj.strftime('%Y-%m-%d')} {date_obj.strftime('%a')}"
            except:
                date_str = event['date']
            
            # Get fields
            title = event.get('title', 'N/A')
            room = event.get('room', '') or '-'
            group = event.get('group', 'N/A')
            start = event.get('start_time', 'N/A')
            end = event.get('end_time', 'N/A')
            time = f"{start}-{end}"
            lecturer = event.get('lecturer', 'N/A')
            event_type = event.get('type', 'N/A')
            note = event.get('description', '') or '-'
            
            # Truncate if needed
            if len(date_str) > w['date']: date_str = date_str[:w['date']]
            if len(title) > w['title']: title = title[:w['title']-3] + "..."
            if len(group) > w['group']: group = group[:w['group']-3] + "..."
            if len(lecturer) > w['lecturer']: lecturer = lecturer[:w['lecturer']-3] + "..."
            if len(note) > w['note']: note = note[:w['note']-3] + "..."
            
            row = (f"{date_str:<{w['date']}} | {time:<{w['time']}} | {title:<{w['title']}} | "
                   f"{room:<{w['room']}} | {group:<{w['group']}} | {lecturer:<{w['lecturer']}} | "
                   f"{event_type:<{w['type']}} | {note:<{w['note']}}")
            print(row)
        
        print("=" * 160 + "\n")


class JSONExporter:
    """Export events to JSON format"""
    
    @staticmethod
    def export(events, filename=None):
        """Export events to JSON file"""
        if filename is None:
            filename = config.OUTPUT["json_file"]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2, ensure_ascii=False)
        
        print(f"Events exported to {filename}")
        return filename


class ICSExporter:
    """Export events to ICS (iCalendar) format with proper timezone support"""
    
    @staticmethod
    def export(events, filename=None):
        """Export events to ICS file"""
        if not HAS_ICS:
            print("Error: ICS export requires 'ics' package. Install with: pip install ics")
            return None
        
        if filename is None:
            filename = config.OUTPUT["ics_file"]
        
        # Try to get timezone
        try:
            import pytz
            timezone = pytz.timezone(config.GOOGLE_CALENDAR["timezone"])
            has_timezone = True
        except ImportError:
            print("Warning: pytz not installed. Timezone info will not be included in ICS file.")
            has_timezone = False
        
        calendar = Calendar()
        success_count = 0
        
        for event_data in events:
            event = Event()
            
            # Set title
            event.name = event_data.get('title', 'Untitled Event')
            
            # Parse date and time
            date_str = event_data.get('date', '')
            start_time_str = event_data.get('start_time', '00:00')
            end_time_str = event_data.get('end_time', '00:00')
            
            try:
                # Create datetime objects
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                start_time = datetime.strptime(start_time_str, "%H:%M" if ':' in start_time_str else "%H:%M:%S")
                end_time = datetime.strptime(end_time_str, "%H:%M" if ':' in end_time_str else "%H:%M:%S")
                
                # Combine date and time - create naive datetime first
                start_datetime_naive = date_obj.replace(hour=start_time.hour, minute=start_time.minute)
                end_datetime_naive = date_obj.replace(hour=end_time.hour, minute=end_time.minute)
                
                # Make timezone-aware to properly handle DST
                if has_timezone:
                    start_datetime = timezone.localize(start_datetime_naive)
                    end_datetime = timezone.localize(end_datetime_naive)
                else:
                    start_datetime = start_datetime_naive
                    end_datetime = end_datetime_naive
                
                event.begin = start_datetime
                event.end = end_datetime
                success_count += 1
                
            except Exception as e:
                print(f"Warning: Could not parse date/time for event '{event_data.get('title', 'Unknown')}': {e}")
                continue
            
            # Set description
            description_parts = []
            if event_data.get('lecturer'):
                description_parts.append(f"Lecturer: {event_data['lecturer']}")
            if event_data.get('room'):
                description_parts.append(f"Room: {event_data['room']}")
            if event_data.get('group'):
                description_parts.append(f"Group: {event_data['group']}")
            if event_data.get('description'):
                description_parts.append(f"Note: {event_data['description']}")
            
            event.description = "\n".join(description_parts)
            
            # Set location
            if event_data.get('room'):
                event.location = f"Room {event_data['room']}, TSI"
            
            # Add event to calendar
            calendar.events.add(event)
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(calendar)
        
        print(f"Events exported to {filename} (ICS format) - {success_count} events")
        return filename


class GoogleCalendarExporter:
    """Export events to Google Calendar"""
    
    def __init__(self):
        self.service = None
        self.calendar_id = config.GOOGLE_CALENDAR["calendar_id"]
        # Import pytz for timezone handling
        try:
            import pytz
            self.pytz = pytz
            self.timezone = pytz.timezone(config.GOOGLE_CALENDAR["timezone"])
        except ImportError:
            print("Warning: pytz not installed. Timezone handling may be incorrect.")
            print("Install with: pip install pytz")
            self.pytz = None
            self.timezone = None
    
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        import os
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        
        token_file = config.GOOGLE_CALENDAR["token_file"]
        credentials_file = config.GOOGLE_CALENDAR["credentials_file"]
        
        # Load existing credentials
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
        print("Google Calendar authentication successful")
    
    def clear_calendar(self, start_date=None, end_date=None):
        """Clear events from calendar in date range"""
        if not self.service:
            self.authenticate()
        
        if start_date is None:
            start_date = datetime(datetime.now().year, 1, 1).isoformat() + 'Z'
        if end_date is None:
            end_date = datetime(datetime.now().year, 12, 31, 23, 59, 59).isoformat() + 'Z'
        
        print(f"Fetching events to delete from Google Calendar...")
        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        for event in events:
            self.service.events().delete(calendarId=self.calendar_id, eventId=event['id']).execute()
            print(f"Deleted: {event.get('summary', 'Untitled')}")
        
        print(f"Cleared {len(events)} events from calendar")
    
    def export(self, events, clear_first=True):
        """Export events to Google Calendar with proper DST handling"""
        if not self.service:
            self.authenticate()
        
        if clear_first:
            self.clear_calendar()
        
        timezone_str = config.GOOGLE_CALENDAR["timezone"]
        location = config.GOOGLE_CALENDAR["location"]
        
        success_count = 0
        error_count = 0
        
        for event_data in events:
            # Parse date and time
            date_str = event_data.get('date', '')
            start_time_str = event_data.get('start_time', '00:00')
            end_time_str = event_data.get('end_time', '00:00')
            
            try:
                # Create datetime objects
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                start_time = datetime.strptime(start_time_str, "%H:%M" if ':' in start_time_str else "%H:%M:%S")
                end_time = datetime.strptime(end_time_str, "%H:%M" if ':' in end_time_str else "%H:%M:%S")
                
                # Combine date and time - create naive datetime first
                start_datetime_naive = date_obj.replace(hour=start_time.hour, minute=start_time.minute)
                end_datetime_naive = date_obj.replace(hour=end_time.hour, minute=end_time.minute)
                
                # Make timezone-aware using pytz to properly handle DST
                if self.timezone and self.pytz:
                    # Use localize() to properly handle DST transitions
                    # This will automatically determine if DST is active for the given date
                    start_datetime = self.timezone.localize(start_datetime_naive)
                    end_datetime = self.timezone.localize(end_datetime_naive)
                else:
                    # Fallback: use naive datetime (not recommended)
                    start_datetime = start_datetime_naive
                    end_datetime = end_datetime_naive
                
                # Create event body
                event_body = {
                    'summary': event_data.get('title', 'Untitled Event'),
                    'location': location,
                    'description': f"Lecturer: {event_data.get('lecturer', 'N/A')}\n"
                                   f"Room: {event_data.get('room', 'N/A')}\n"
                                   f"Group: {event_data.get('group', 'N/A')}\n"
                                   f"Note: {event_data.get('description', '')}",
                    'start': {
                        'dateTime': start_datetime.isoformat(),
                        'timeZone': timezone_str,
                    },
                    'end': {
                        'dateTime': end_datetime.isoformat(),
                        'timeZone': timezone_str,
                    },
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'popup', 'minutes': 15},
                        ],
                    },
                }
                
                # Insert event
                self.service.events().insert(calendarId=self.calendar_id, body=event_body).execute()
                success_count += 1
                
                # Show progress every 10 events
                if success_count % 10 == 0:
                    print(f"Progress: {success_count}/{len(events)} events exported...")
                
            except Exception as e:
                error_count += 1
                print(f"Warning: Could not export event '{event_data.get('title', 'Unknown')}' on {date_str}: {e}")
        
        print(f"\n✓ Successfully exported {success_count} events to Google Calendar")
        if error_count > 0:
            print(f"✗ Failed to export {error_count} events")

