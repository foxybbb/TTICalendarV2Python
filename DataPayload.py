from datetime import datetime,timezone
schedule_data= {
    'time_from': '1709327101', # Time unix format https://www.unixtimestamp.com/
    'time_to': '1719864301',
    'teachers': '',
    'rooms': '',
    'group': '3301-2MDA',  # Change group number
    'lang': 'en'
}

google_caledar= {
    'calendar_id':'xxxxxxxxxxxxxxxxxxxxxxxxxx@group.calendar.google.com', # change for your calendar
}

settings = {
    'debug_messages': True,
    'delete_calendar_event_start_date': datetime(datetime.now().year, 1, 1, tzinfo=timezone.utc).isoformat(),
    'delete_calendar_event_end_date': datetime(datetime.now().year, 12, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat()

}