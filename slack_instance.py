import os
import slack
from slackeventsapi import SlackEventAdapter

class SlackInstance:
    def __init__ (self, server):
        self.signing_secret = os.environ['signing_secret']
        self.token = os.environ['slack_token']
        self.endpoint = os.environ['slack_endpoint']
        self.server = server
        self.web_client = slack.WebClient(token=self.token)
    def get_event_adapter(self):
        return SlackEventAdapter(signing_secret=self.signing_secret, server = self.server, endpoint=self.endpoint)
    def get_web_client(self):
        return self.web_client
    def get_bot_id(self):
       return self.web_client.api_call('auth.test')['user_id']
    def get_channel_info(self, channel_id):
       channel_info = self.web_client.api_call('conversations.info', params={'channel': channel_id})['channel']
       return {
           'name': channel_info['name'],
           'description': channel_info['purpose']['value']
       }
    def _get_profile_information(self, key, user_id):
        data = self.web_client.api_call(api_method='users.info', params={'user': user_id})
        return data['user']['profile'][key]
    def get_user_email(self, user_id):
        email = self._get_profile_information('email', user_id)
        return email
    def get_user_role(self, user_id):
        role = self._get_profile_information('title', user_id)
        return role