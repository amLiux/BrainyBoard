import os
import slack
from slackeventsapi import SlackEventAdapter

class SlackInstance:
    def __init__ (self, server):
        self.signing_secret = os.environ['signing_secret']
        self.token = os.environ['slack_token']

        self.server = server
        self.endpoint = '/slack/events'
        self.web_client = slack.WebClient(token=self.token)
    def get_event_adapter(self):
        return SlackEventAdapter(signing_secret=self.signing_secret, server = self.server, endpoint=self.endpoint)
    def get_web_client(self):
        return self.web_client
    def get_bot_id(self):
       return self.web_client.api_call('auth.test')['user_id']