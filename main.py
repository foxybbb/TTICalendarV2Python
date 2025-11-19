#!/usr/bin/env python3
"""
TSI Calendar Scraper - Main Entry Point
Fetch calendar data and export to various formats
"""

from TSICalendar import TSICalendar, sort_events, filter_events
from Exporters import TableExporter, JSONExporter, ICSExporter, GoogleCalendarExporter
import config


def main():
    """Main entry point"""
    print("=" * 80)
    print("TSI Calendar Scraper")
    print("=" * 80)
    
    calendar = TSICalendar()
    
    try:
        # Step 1: Login
        print("\nStep 1: Authenticating...")
        calendar.login()
        
        # Step 2: Fetch calendar data
        print(f"\nStep 2: Fetching calendar data")
        print(f"Date range: {config.DATE_RANGE['from_year']}-{config.DATE_RANGE['from_month']:02d} "
              f"to {config.DATE_RANGE['to_year']}-{config.DATE_RANGE['to_month']:02d}")
        print(f"Filters: Room={config.FILTERS['room']}, Lecturer={config.FILTERS['lecturer']}, "
              f"Group={config.FILTERS['group']}")
        print("-" * 80)
        
        events = calendar.fetch_period(
            config.DATE_RANGE['from_year'],
            config.DATE_RANGE['from_month'],
            config.DATE_RANGE['to_year'],
            config.DATE_RANGE['to_month']
        )
        
        print(f"\nTotal events fetched: {len(events)}")
        
        # Step 3: Filter and sort
        print(f"\nStep 3: Processing events")
        events = filter_events(events)
        events = sort_events(events, config.DISPLAY['sort_by'])
        
        print(f"After filtering: {len(events)} events")
        print(f"Sorting by: {config.DISPLAY['sort_by']}")
        
        if not events:
            print("\nNo events found matching the criteria")
            return
        
        # Step 4: Export to requested formats
        print(f"\nStep 4: Exporting to formats: {', '.join(config.OUTPUT['formats'])}")
        print("-" * 80)
        
        for format_type in config.OUTPUT['formats']:
            format_type = format_type.lower().strip()
            
            if format_type == "table":
                TableExporter.export(events)
            
            elif format_type == "json":
                JSONExporter.export(events)
            
            elif format_type == "ics":
                ICSExporter.export(events)
            
            elif format_type == "google_calendar":
                try:
                    google_exporter = GoogleCalendarExporter()
                    google_exporter.export(events, clear_first=True)
                except ImportError:
                    print("Error: Google Calendar export requires google-auth, google-auth-oauthlib, "
                          "and google-api-python-client packages")
                except Exception as e:
                    print(f"Error exporting to Google Calendar: {e}")
            
            else:
                print(f"Warning: Unknown export format '{format_type}'")
        
        print("\n" + "=" * 80)
        print("Export completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        calendar.close()


if __name__ == "__main__":
    main()
