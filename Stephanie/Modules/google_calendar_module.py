import pytz
import datetime
import re

import httplib2

from Stephanie.Modules.base_module import BaseModule
# noinspection PyUnresolvedReferences
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import *


# Written by Marc Poul Joseph Laventure

class GoogleCalendarModule(BaseModule):
    def __init__(self, *args):
        super(GoogleCalendarModule, self).__init__(*args)
        self.client_id = self.get_configuration("google_calendar_client_id")
        self.client_secret = self.get_configuration("google_calendar_client_secret")
        self.service = None
        self.month_dict = None
        if self.client_id and self.client_secret:
            self.do_init()
        else:
            return False

    def do_init(self):
        # The scope URL for read/write access to a user's calendar data
        scope = 'https://www.googleapis.com/auth/calendar'
        # Create a flow object. This object holds the client_id, client_secret, and
        # scope. It assists with OAuth 2.0 steps to get user authorization and
        # credentials.

        flow = OAuth2WebServerFlow(self.client_id, self.client_secret, scope)

        # Create a Storage object. This object holds the credentials that your
        # application needs to authorize access to the user's data. The name of the
        # credentials file is provided. If the file does not exist, it is
        # created. This object can only hold credentials for a single user, so
        # as-written, this script can only handle a single user.
        storage = Storage('credentials.dat')

        # The get() function returns the credentials for the Storage object. If no
        # credentials were found, None is returned.
        credentials = storage.get()

        # If no credentials are found or the credentials are invalid due to
        # expiration, new credentials need to be obtained from the authorization
        # server. The oauth2client.tools.run_flow() function attempts to open an
        # authorization server page in your default web browser. The server
        # asks the user to grant your application access to the user's data.
        # If the user grants access, the run_flow() function returns new credentials.
        # The new credentials are also stored in the supplied Storage object,
        # which updates the credentials.dat file.
        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        # Create an httplib2.Http object to handle our HTTP requests, and authorize it
        # using the credentials.authorize() function.
        http = httplib2.Http()

        http = credentials.authorize(http)

        # The apiclient.discovery.build() function returns an instance of an API service
        # object can be used to make API calls. The object is constructed with
        # methods specific to the calendar API. The arguments provided are:
        #   name of the API ('calendar')
        #   version of the API you are using ('v3')
        #   authorized httplib2.Http() object that can be used for API calls
        self.service = build('calendar', 'v3', http=http)
        self.month_dict = {'January': '01',
                           'February': '02',
                           'March': '03',
                           'April': '04',
                           'May': '05',
                           'June': '06',
                           'July': '07',
                           'August': '08',
                           'September': '09',
                           'October': '10',
                           'November': '11',
                           'December': '12'}

    def add_event(self):
        while True:
            try:
                self.assistant.say("What would you like to add?")
                event_data = self.assistant.listen().decipher()
                created_event = self.service.events().quickAdd(calendarId='primary', text=event_data) \
                    .execute()
                event_raw_start_time = created_event['start']

                stupid_variable = re.search('([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})',
                                            str(event_raw_start_time))
                # event_date_year = str(stupid_variable.group(1))
                event_date_month = str(stupid_variable.group(2))
                event_date_day = str(stupid_variable.group(3))
                event_time_hour = str(stupid_variable.group(4))
                event_time_minute = str(stupid_variable.group(5))
                appending_time = "am"

                if len(event_time_minute) == 1:
                    event_time_minute += "0"

                event_time_hour = int(event_time_hour)

                if (event_time_hour - 12) > 0:
                    event_time_hour -= 12
                    appending_time = "pm"

                dict_keys = [key for key, val in self.month_dict.items() if val == event_date_month]
                event_date_month = dict_keys[0]
                self.assistant.say(
                    "Added event " + created_event['summary'] + " on " + str(event_date_month) + " " + str(
                        event_date_day) + " at " + str(event_time_hour) + ":" + str(
                        event_time_minute) + " " + appending_time
                )
                self.assistant.say("Is this what you wanted?")
                user_response = self.assistant.listen().decipher()

                if bool(re.search('Yes', user_response, re.IGNORECASE)):
                    return "Okay, I added it to your calendar"

                self.service.events().delete(calendarId='primary', eventId=created_event['id']).execute()

            except KeyError:

                self.assistant.say("Could not add event to your calender; check if internet issue.")
                self.assistant.say("Would you like to attempt again?")
                response_redo = self.assistant.listen().decipher()

                if bool(re.search('No', response_redo, re.IGNORECASE)):
                    return "Alright then."

    def get_events_today(self):
        # Get Present Start Time and End Time in RFC3339 Format
        timestamp = datetime.datetime.now(tz=pytz.utc)
        utc_string = timestamp.isoformat()
        another_stupid_variable = re.search('((\+|\-)[0-9]{2}:[0-9]{2})', str(utc_string))
        utc_string = str(another_stupid_variable.group(0))
        today_start_time = str(timestamp.strftime("%Y-%m-%d")) + "T00:00:00" + utc_string
        today_end_time = str(timestamp.strftime("%Y-%m-%d")) + "T23:59:59" + utc_string
        token_page = None

        while True:

            # Gets events from primary calender from each page in present day boundaries
            events_found = self.service.events().list(calendarId='primary', pageToken=token_page,
                                                      timeMin=today_start_time, timeMax=today_end_time).execute()

            if len(events_found['items']) == 0:
                return "You have no events scheduled for today"

            for event_found in events_found['items']:

                try:
                    event_title = event_found['summary']
                    event_title = str(event_title)
                    event_raw_start_time = event_found['start']
                    event_raw_start_time = event_raw_start_time['dateTime'].split("T")
                    temp_stupid_variable = event_raw_start_time[1]
                    start_hour, start_minute, temp_stupid_variable = temp_stupid_variable.split(":", 2)
                    start_hour = int(start_hour)
                    appending_time = "am"

                    if (start_hour - 12) > 0:
                        start_hour -= 12
                        appending_time = "pm"

                    start_minute = str(start_minute)
                    start_hour = str(start_hour)
                    self.assistant.say(
                        event_title +
                        " at " +
                        start_hour +
                        ":" +
                        start_minute +
                        " " +
                        appending_time
                    )  # This will be self.assistant.say

                except KeyError:
                    self.assistant.say("Check Calender that you added it correctly")

            token_page = events_found.get('nextPageToken')

            if not token_page:
                return "That's it."

    def get_events_tomorrow(self):

        # Time Delta function for adding one day

        one_day = datetime.timedelta(days=1)

        # Gets tomorrows Start and End Time in RFC3339 Format

        d = datetime.datetime.now(tz=pytz.utc) + one_day
        utc_string = d.isoformat()
        m = re.search('((\+|\-)[0-9]{2}:[0-9]{2})', str(utc_string))
        utc_string = m.group(0)
        tomorrow_start_time = str(d.strftime("%Y-%m-%d")) + "T00:00:00" + utc_string
        tomorrow_end_time = str(d.strftime("%Y-%m-%d")) + "T23:59:59" + utc_string

        page_token = None

        while True:

            # Gets events from primary calender from each page in tomorrow day boundaries

            events = self.service.events().list(
                calendarId='primary',
                pageToken=page_token,
                timeMin=tomorrow_start_time,
                timeMax=tomorrow_end_time
            ).execute()
            if len(events['items']) == 0:
                return "You have no events scheduled Tomorrow"

            for event in events['items']:

                try:
                    event_title = event['summary']
                    event_title = str(event_title)
                    event_raw_start_time = event['start']
                    event_raw_start_time = event_raw_start_time['dateTime'].split("T")
                    temp = event_raw_start_time[1]
                    start_hour, start_minute, temp = temp.split(":", 2)
                    start_hour = int(start_hour)
                    appending_time = "am"

                    if (start_hour - 12) > 0:
                        start_hour -= 12
                        appending_time = "pm"

                    start_minute = str(start_minute)
                    start_hour = str(start_hour)
                    self.assistant.say(
                        event_title + " at " +
                        start_hour + ":" +
                        start_minute +
                        " " + appending_time
                    )  # This will be self.assistant.say

                except KeyError:
                    self.assistant.say("Check Calender that you added it correctly")

            page_token = events.get('nextPageToken')

            if not page_token:
                return "That's it."
