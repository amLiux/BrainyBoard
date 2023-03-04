from slack_instance import SlackInstance
from brainy_board import BrainyBoard
from trello import Trello
brainy_board = BrainyBoard()
# these loads env for every Class used later on
brainy_board.load_env()
http_utils = brainy_board.get_http_utils()
response, request = http_utils.get('response'), http_utils.get('request')

# initialize flask
app = brainy_board.init_app()

# initialize trello provider
trello_provider = Trello()

# initiating slack web client
slack = SlackInstance(app)
client = slack.get_web_client()
slack_adapter = slack.get_event_adapter()
bot_id = slack.get_bot_id()

@slack_adapter.on('message')
def message_received(payload):
    event = payload.get('event', {})
    text, user_id, channel_id = event.get('text'), event.get('user'), event.get('channel')
    print(payload)
    if bot_id != user_id:
        client.chat_postMessage(channel=channel_id, text=text)

@app.route('/lists', methods=['POST'])
def get_lists():
    payload = request.form
    channel_id = payload.get('channel_id')
    data = trello_provider.get_all_lists()
    client.chat_postMessage(channel=channel_id, text=data)
    return response(), 200


if __name__ == "__main__":
    app.run(debug=True)