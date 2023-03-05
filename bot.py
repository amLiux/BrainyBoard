from slack_instance import SlackInstance
from brainy_board import BrainyBoard
from trello import Trello
from text import TranslationProvider
from welcome_message import WelcomeMessage

brainy_board = BrainyBoard()
# this loads env for every Class used later on
brainy_board.load_env()
http_utils = brainy_board.get_http_utils()
response, request = http_utils.get('response'), http_utils.get('request')
translation_provider = TranslationProvider()

# initialize flask
app = brainy_board.init_app()

# initialize trello provider
trello_provider = Trello()

# initiating slack web client
slack = SlackInstance(app)
client = slack.get_web_client()
slack_adapter = slack.get_event_adapter()
bot_id = slack.get_bot_id()

lists = trello_provider.lists

def send_welcome_message(channel, user):
    channel_info = slack.get_channel_info(channel_id=channel)
    channel_name, channel_description = channel_info['name'], channel_info['description']
    welcome = WelcomeMessage(translation_provider, channel_name, user, channel_description=channel_description)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    welcome.timestampp = response['ts']

@slack_adapter.on('message')
def message_received(payload):
    event = payload.get('event', {})
    text, user_id, channel_id, subtype = event.get('text'), event.get('user'), event.get('channel'), event.get('subtype')

    if subtype == 'channel_join':
        send_welcome_message(channel_id, user_id)

    if bot_id != user_id:
        client.chat_postMessage(channel=channel_id, text=text)

@app.route('/lists', methods=['POST'])
def get_lists():
    payload = request.form
    channel_id = payload.get('channel_id')
    to_return = []
    for list in lists:
        to_return.append(list.get('name'))
    lists_message = translation_provider.translate('LISTS_MESSAGE');
    client.chat_postMessage(channel=channel_id, text=f'{lists_message} \n' + ", \n".join(to_return))
    return response(), 200

@app.route('/tickets', methods=['POST'])
def get_tickets_by_asignee():
    payload = request.form
    channel_id, user_id, text = payload.get('channel_id'), payload.get('user_id'), payload.get('text')
    if text == '':
        error_message = translation_provider.translate('NOT_BOARD_ERROR')
        client.chat_postMessage(channel=channel_id, text=error_message)
        return response(), 500
    user_email = slack.get_user_email(user_id=user_id)
    searching_message = translation_provider.translate('SEARCHING_TICKETS_MESSAGE');
    searching_message = searching_message.replace('{user_email}', user_email).replace('{text}', text)
    client.chat_postMessage(channel=channel_id, text=searching_message)
    return response(), 200


if __name__ == "__main__":
    app.run(debug=True)