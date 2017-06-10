from Stephanie.Modules.base_module import BaseModule
import tweepy
# from tweepy.streaming import StreamListener
# from tweepy import OAuthHandler
# from tweepy import Stream
from tweepy import *


# used quite long snippets from https://github.com/marclave/Jasper-Twitter/blob/master/Twitter.py
# written by Marc Laventure, thank you mark, you're the man! *hugs*

class TwitterModule(BaseModule):
    def __init__(self, *args):
        super(TwitterModule, self).__init__(*args)
        self.consumer_key = self.get_configuration("twitter_consumer_key")
        self.consumer_secret = self.get_configuration("twitter_consumer_secret")
        self.access_token = self.get_configuration("twitter_access_token")
        self.access_token_secret = self.get_configuration("twitter_access_token_secret")
        self.auth = None
        self.api = None
        self.myTwitterID = None
        if self.consumer_key and self.consumer_secret and self.access_token and self.access_token_secret:
            self.do_init()
        else:
            return False

    def do_init(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.myTwitterID = self.api.me().id

    def get_trending(self):
        print(self.api)
        data = self.api.trends_place(1)  # Grabs global trends
        trends = data[0]['trends']
        for index, trend in enumerate(trends):
            if index < 5:
                name = trend['name']  # Grabs name of each trend
                if name.startswith('#'):
                    self.assistant.say(name)  # Only grabs hashtags
        return "these were the top 5 trends on twitter globally."

    def status_update(self):
        self.assistant.say("What would you like to tweet?")
        tweet = self.assistant.listen().decipher()
        self.api.update_status(tweet)
        return "%s has been tweeted" % tweet

    def get_notifications(self):
        latest_retweets = []
        latest_retweets_id = []
        # latest_direct_messages = []
        # latest_direct_messages_id = []
        latest_mentions = []
        latest_mentions_id = []

        mentions = self.api.mentions_timeline(count=1)
        retweets = self.api.retweets_of_me(count=1)
        # direct_messages = self.api.direct_messages(count=1)

        for mention in mentions:
            latest_mentions.append(mention)
            latest_mentions_id.append(mention.id)

        for retweet in retweets:
            latest_retweets.append(retweet)
            latest_retweets_id.append(retweet.id)
        #
        # for directMessage in direct_messages:
        #     latest_direct_messages.append(directMessage)
        #     latest_direct_messages_id.append(directMessage.id)
        response = ""
        if len(latest_retweets) > 0:
            response += "Latest Retweets are "
            for retweetFinal in latest_retweets:
                response += (retweetFinal.text + " by " + retweetFinal.user.screen_name + ". ")
        else:
            response += ("You have no re-tweets. ")

        if len(latest_mentions) > 0:
            response += ("Latest Mentions are ")

            for mentionFinal in latest_mentions:
                response += (mentionFinal.text + " from " + mentionFinal.user.screen_name + ". ")

        else:
            response += ("You have no mentions. ")

        # if len(latest_direct_messages) > 0:
        #     self.assistant.say("Latest Direct Messages are")
        #
        #     for directMessageFinal in latest_direct_messages:
        #         self.assistant.say(directMessageFinal.text + " from " + directMessageFinal.user.screen_name)
        #
        # else:
        #     self.assistant.say("You have no Direct Messages")
        response += "These were the latest notifications."
        return response
