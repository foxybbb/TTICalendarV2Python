import requests
from xml.etree import ElementTree as ET
from DataPayload import schedule_data,settings
import os.path
import json
import time


def get_data():
    url = 'https://services.tsi.lv/schedule/api/service.asmx/GetLocalizedEvents?from={}' \
          '&to={}&teachers={}&rooms={}&groups={}&lang={}'.format(schedule_data['time_from'],
                                                                 schedule_data['time_to'],
                                                                 schedule_data['teachers'],
                                                                 schedule_data['rooms'],
                                                                 schedule_data['group'],
                                                                 schedule_data['lang'])

    headers = {
        "Accept": "text/plain",
        "Content-Type": "text/plain",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip"
    }
    # if settings['debug_messages']:
    print(url)
    return requests.get(url, headers=headers)


def get_request(url):
    headers = {
        "User-Agent": "okhttp/3.12.1",
        "Content-Type": "xml",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip"
    }
    return requests.get(url, headers=headers)


def get_key_by_name(json, group, name):
    # Parse the JSON string into a Python dictionary
    data = json

    # Assuming 'teachers' is a top-level key in your JSON structure
    teachers_dict = data[group]

    # Iterate through the dictionary and search for the name
    for key, value in teachers_dict.items():
        if value == name:
            return key
    return ''


def get_name_by_key(json, group, key):
    data = json
    teachers_dict = data[group]
    for name, value in teachers_dict.items():
        if name == key:
            return value
    return ''


class Rest:

    def __init__(self):
        self.lesson_list = None
        self.get_tsi_data()
        if os.path.exists("shedule.json"):
            with open("shedule.json", 'r') as f:
                self.shedule_data = json.load(f)
        else:
            self.shedule_data = self.get_schedule_data()
            with open("shedule.json", "w") as f:
                json.dump(self.shedule_data, f)

    def get_tsi_data(self):
        if not (os.path.exists("tsi_data.json")):
            response = get_request('https://services.tsi.lv/schedule/api/service.asmx/GetItems')
            if response.status_code == 200:
                self.tsi_data = json.loads(ET.fromstring(response.text).text)
                self.tsi_data['timestamp'] = int(time.time())

                with open("tsi_data.json", "w") as f:
                    json.dump(self.tsi_data, f)
        else:
            print("tsi_data.json found")
            with open("tsi_data.json", 'r') as f:
                self.tsi_data = json.load(f)

            if (time.time() - self.tsi_data['timestamp']) >= (7 * 24 * 60 * 60):
                response = get_request('https://services.tsi.lv/schedule/api/service.asmx/GetItems')
                if response.status_code == 200:
                    self.tsi_data = json.loads(ET.fromstring(response.text).text)
                    self.tsi_data['timestamp'] = int(time.time())

    def get_schedule_data(self):

        url = ('https://services.tsi.lv/schedule/api/service.asmx/GetLocalizedEvents?from={}'
               '&to={}&teachers={}&rooms={}&groups={}&lang={}').format(schedule_data['time_from'],
                                                                       schedule_data['time_to'],get_key_by_name(self.tsi_data, 'teachers', schedule_data['teachers']),
                                                                       get_key_by_name(self.tsi_data, 'rooms',
                                                                                       schedule_data['rooms']),
                                                                       get_key_by_name(self.tsi_data, 'groups',
                                                                                       schedule_data['group']),
                                                                       schedule_data['lang'])
        if settings['debug_messages']:
            print(url)
        response = get_request(url)
        # response = self.__get_request(url)

        if response.status_code == 200:
            tsi_data = json.loads(ET.fromstring(response.text).text)
        else:
            return None
        return tsi_data

    def update_schedule(self):
        self.lesson_list = self.shedule_data['events']['values']

    def get_lesson_list(self):
        for lesson in self.lesson_list:
            lesson[1] = get_name_by_key(self.tsi_data, 'rooms', str(lesson[1][0]))
            if schedule_data['teachers'] == '':
                lesson[2] = get_name_by_key(self.tsi_data, 'groups', str(lesson[2][0]))
            else:
                lesson[2] = get_name_by_key(self.tsi_data, 'groups', str(lesson[2]))

            lesson[3] = get_name_by_key(self.tsi_data, 'teachers', str(lesson[3]))

        return self.lesson_list
