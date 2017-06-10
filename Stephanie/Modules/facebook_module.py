import pytz
import datetime
import requests
import facebook
from Stephanie.Modules.base_module import BaseModule


class FacebookModule(BaseModule):
    def __init__(self, *args):
        super(FacebookModule, self).__init__(*args)
        self.oauth_access_token = self.get_configuration('facebook_oauth_token')
        self.requests = requests
        if self.oauth_access_token:
            self.graph = None
            self.set_graph()
        else:
            status = self.do_init()
            if not status:
                return False

    def do_init(self):
        app_id = self.get_configuration('facebook_app_id')
        app_secret = self.get_configuration('facebook_app_secret')
        app_access_token = self.get_configuration('facebook_access_token')
        if app_id and app_secret and app_access_token:
            params = {
                'client_id': app_id,
                'client_secret': app_secret,
                'grant_type': 'fb_exchange_token',
                'fb_exchange_token': app_access_token
            }
            r = self.requests.get("https://graph.facebook.com/oauth/access_token", params=params)
            if r.ok:
                oauth_access_token = r.json()['access_token']
                self.oauth_access_token = self.write_configuration('facebook_oauth_token', oauth_access_token)
                self.graph = facebook.GraphAPI(oauth_access_token)
                return True
        return False

    def set_graph(self, oauth_access_token=None):
        if oauth_access_token:
            self.oauth_access_token = oauth_access_token
        self.graph = facebook.GraphAPI(self.oauth_access_token)

    def get_birthday_reminders(self):
        """
            Responds to user-input, typically speech text, by listing the user's
            Facebook friends with birthdays today.
            Arguments:
            text -- user-input, typically transcribed speech
            self.assistant -- used to interact with the user (for both input and output)
            profile -- contains information related to the user (e.g., phone
                       number)
        """
        try:
            results = self.graph.request("me/friends",
                                         args={'fields': 'id,name,birthday'})
        except facebook.GraphAPIError:
            response = ("I have not been authorized to query your Facebook. If you " +
                        "would like to check birthdays in the future, please visit " +
                        "the Jasper dashboard.")
            return response
        except:
            return "I apologize, there's a problem with that service at the moment."

        needle = datetime.datetime.now(tz=pytz.utc).strftime("%m/%d")

        people = []
        for person in results['data']:
            try:
                if needle in person['birthday']:
                    people.append(person['name'])
            except:
                continue

        if len(people) > 0:
            if len(people) == 1:
                output = people[0] + " has a birthday today."
            else:
                output = "Your friends with birthdays today are " + \
                         ", ".join(people[:-1]) + " and " + people[-1] + "."
        else:
            output = "None of your friends have birthdays today."

        return output

    def get_notifications(self):
        """
            Not working since facebooks new update which doesn't allow notifications to be fetched. :(
            Responds to user-input, typically speech text, with a summary of
            the user's Facebook notifications, including a count and details
            related to each individual notification.

            Arguments:
            text -- user-input, typically transcribed speech
            self.assistant -- used to interact with the user (for both input and output)
            profile -- contains information related to the user (e.g., phone
                       number)
        """
        try:
            results = self.graph.request("me/notifications")
        except facebook.GraphAPIError:
            response = ("I have not been authorized to query your Facebook. If you " +
                        "would like to check your notifications in the future, " +
                        "please visit the Stephanie facebook module configuraton.")
            return response
        except:
            return "I apologize, there's a problem with that service at the moment."
        if not len(results['data']):
            return "You have no Facebook notifications."

        updates = []
        for notification in results['data']:
            updates.append(notification['title'])

        count = len(results['data'])
        response = ("You have " + str(count) +
                    " Facebook notifications. " + " ".join(updates) + ". ")

        return response

    def status_update(self):
        self.assistant.say("What's in your mind?")
        text = self.assistant.listen().decipher()
        try:
            self.graph.put_wall_post(text)
            self.assistant.say("You have successully put up a wall post.")
        except facebook.GraphAPIError:
            response = ("I have not been authorized to query your Facebook. If you " +
                        "would like to check your notifications in the future, " +
                        "please visit the Stephanie facebook module configuraton.")
            return response
        except:
            return "I apologize, there's a problem with that service at the moment."
