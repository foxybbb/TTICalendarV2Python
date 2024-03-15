import os
import pickle
from os.path import isfile

from Request import Rest

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone, timedelta
from DataPayload import google_caledar,settings,schedule_data
import pytz
def authenticate_google_calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # 'credentials.json' is the downloaded JSON file.
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_lesson_description(lesson_data):
    return 'Лектор: {}\nАудитория: {}\nПримечание: {}'.format(lesson_data[3], lesson_data[1], lesson_data[5])


def get_calendar_id():
    return google_caledar['calendar_id']


def get_event_body(lesson_data):
    time_zone = 'Europe/Riga'
    TSI_Location = 'Институт транспорта и связи, Lomonosova iela 1, Latgales priekšpilsēta, Rīga, LV-1019, Латвия'

    start_time = datetime.fromtimestamp(lesson_data[0]-7200, tz=timezone.utc)
    end_time = start_time + timedelta(hours=1, minutes=30)
    return {
        'summary': lesson_data[4],
        'location': TSI_Location,
        'description': get_lesson_description(lesson_data),
        'start': {
            'dateTime': datetime.isoformat(start_time),
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': datetime.isoformat(end_time),
            'timeZone': time_zone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }


class CalendarExporter:
    def __init__(self):
        self.service = authenticate_google_calendar()
        self.calendar_id = get_calendar_id()
        self.rq = Rest()

    def update_calendar(self):
        self.rq.update_schedule()
        self.clear_calendar()
        self.fill_calendar()
        self.delete_shedule_data()

    def create_event(self, lesson_data):
        self.service.events().insert(calendarId=self.calendar_id, body=get_event_body(lesson_data)).execute()
    def clear_all_calendar(self):
        events_result = self.service.events().list(calendarId=get_calendar_id(), singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            # Deleting the event
            self.service.events().delete(calendarId=get_calendar_id(), eventId=event['id']).execute()
            if settings['debug_messages']:
                print(f"Event '{event['summary']}' deleted.")
    def clear_calendar(self):

        start_of_year = settings['delete_calendar_event_start_date']
        end_of_year = settings['delete_calendar_event_end_date']
        if settings['debug_messages']:
            print('Fetching events for this year')
        events_result = self.service.events().list(calendarId=get_calendar_id(), timeMin=start_of_year,
                                              timeMax=end_of_year, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        for event in events:
                # Deleting the event
                self.service.events().delete(calendarId=get_calendar_id(), eventId=event['id']).execute()
                if settings['debug_messages']:
                    print(f"Event '{event['summary']}' deleted.")

    def delete_shedule_data(self):
        if os.path.exists('shedule.json'):
            os.remove('shedule.json')

    def fill_calendar(self):
        for lesson_data in self.rq.get_lesson_list():
            self.create_event(lesson_data)
            print(lesson_data)
