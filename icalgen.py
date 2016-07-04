#!/usr/bin/env python3

from icalendar import Calendar as iCalendar, Event
import datetime
import pytz
import requests
import os

# f = open('importio.json', 'rb')
# json = json.loads(f.read().decode())

MOVEAVEIRO_API_ENDPOINT = 'https://api.import.io/store/connector/3efbeeba-cf14-4fdb-af8f-7c6ba6d27f0c/_query?input=webpage/url:https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F12epuwHtZbmF3xpFZydbLVw19xR_c-EDyX2tfzpZTtRo%2Fpubhtml&&_apikey=f2f3cb66f1b6401ebbf5c2a1ba04fdbfb1f94626e5a682059588ee5e282ccb73102540273ee25426ded781d8c39315ddf137df6023b26bcbff811978815bd0e13686a986642c06c408cd4da678cd7aec'
json = requests.get(MOVEAVEIRO_API_ENDPOINT).json()
json = json['results']
ical = iCalendar()

''' Separate results by path '''
paths = {'1': [], '2': [], '3.1': [], '3.2': [], '4': [], '5': []}
for result in json:
    if 'path' in result:
        for k in [k for k in result.keys() if k.startswith("union_")]:
            result[k[6:]] = result[k]
            del result[k]

            paths[result['path']].append(result)

            event = Event()

            # Note
            # http://www.ietf.org/rfc/rfc2445.txt
            # http://icalendar.readthedocs.io

            # # # event['location'] = vText('Aveiro, Portugal')
            event.add('summary', "%s" % result['location'])

            event.add('description', 'By %s' % result['transport_type'])  # <<AI string here>>

            if(result['on'] == 'Working Days'):
                event.add('rrule', {'freq': 'weekly', 'byday': ['MO', 'TU', 'WE', 'TH', 'FR']})
            if(result['on'] == 'Saturdays'):
                event.add('rrule', {'freq': 'weekly', 'byday': ['SA']})
            if(result['on'] == 'Sundays and holidays'):
                event.add('rrule', {'freq': 'weekly', 'byday': ['SU']})

            event.add('dtstart', datetime.datetime(2016, 1, 1, int(result[k[6:]].split(':')[0]), int(result[k[6:]].split(':')[1]), 0, tzinfo=pytz.timezone("Europe/Lisbon")))
            event.add('dtend', datetime.datetime(2016, 12, 31, int(result[k[6:]].split(':')[0]), int(result[k[6:]].split(':')[1]), 0, tzinfo=pytz.timezone("Europe/Lisbon")))
            ical.add_component(event)


f = open(os.path.join('.', 'ma_ical.ics'), 'wb')
f.write(ical.to_ical())
f.close()
# result = ical.to_ical().decode().replace('\r\n', '\n').strip()

# print(result)
