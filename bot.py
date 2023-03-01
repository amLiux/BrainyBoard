from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slack_instance import SlackInstance

class BrainyBoard:
    def __init__(self):
        env_path = Path('.') / '.env'
        self.env_path = env_path

    def load_env(self):
        # loading .env
        load_dotenv(dotenv_path=self.env_path)
    def init_app (self):
        # creating flask app
        return Flask(__name__)

brainy_board = BrainyBoard()
# these loads env for every Class used later on
brainy_board.load_env()
app = brainy_board.init_app()

# initiating slack web client
slack = SlackInstance(app)
client = slack.get_web_client()
slack_adapter = slack.get_event_adapter()
bot_id = slack.get_bot_id()

@slack_adapter.on('message')
def message_received(payload):
    event = payload.get('event', {})
    text, user_id = event.get('text'), event.get('user')
    print(payload)
    if bot_id != user_id:
        client.chat_postMessage(channel='#python-bot-test', text=text)


if __name__ == "__main__":
    app.run(debug=True)