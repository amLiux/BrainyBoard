from slack_instance import SlackInstance
from brainy_board import BrainyBoard
from trello import Trello
from text import TranslationProvider
from welcome_message import WelcomeMessage
from threading import Thread
from openai_instance import OpenAIProvider

brainy_board = BrainyBoard()
# this loads env for every Class used later on
brainy_board.load_env()

# get HTTP utils and descructure them
http_utils = brainy_board.get_http_utils()
response, request = http_utils.get('response'), http_utils.get('request')

# get our translation provider
translation_provider = TranslationProvider()

# get openai provider
openai = OpenAIProvider()

# initialize flask
app = brainy_board.init_app()

# initialize trello provider
trello_provider = Trello()

# initiating slack web client
slack = SlackInstance(app)
client = slack.get_web_client()

# initiating slack event adapter
slack_adapter = slack.get_event_adapter()

# get our bot_id for later
bot_id = slack.get_bot_id()

lists = trello_provider.lists

def get_translated_message(key):
    return translation_provider.translate(key)

def send_welcome_message(channel, user):
    channel_info = slack.get_channel_info(channel_id=channel)
    channel_name, channel_description = channel_info['name'], channel_info['description']
    welcome = WelcomeMessage(translation_provider, channel_name, user, channel_description=channel_description)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    # TODO continue this
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
    lists_message = get_translated_message('LISTS_MESSAGE')
    client.chat_postMessage(channel=channel_id, text=f'{lists_message} \n' + ", \n".join(to_return))
    return response(), 200


@app.route('/tickets', methods=['POST'])
def get_tickets_by_asignee():
    payload = request.form
    # we need to give Slack API a response within 3000ms that's why we create a separate thread and respond
    Thread(target=handle_ticket_command, kwargs=(payload)).start()
    return response(), 200

@app.route('/guidance', methods=['POST'])
def get_gpt_guidance():
    payload = request.form
    # we need to give Slack API a response within 3000ms that's why we create a separate thread and respond
    Thread(target=handle_guidance_command, kwargs=(payload)).start()
    return response(), 200



# TODO add validation and maybe some abstraction for this complex route
def handle_guidance_command(**payload):
    # destructuring stuff
    text, user_id, channel_id = payload.get('text'), payload.get('user_id'), payload.get('channel_id')
    user_role = slack.get_user_role(user_id)
    ticket_information = trello_provider.get_ticket_information(text)
    thinking_message = get_translated_message('THINKING_MESSAGE')
    client.chat_postMessage(channel=channel_id, text=thinking_message)
    chat_gpt_response = openai.ask_chatgpt(
        openai.get_formatted_question(
            user_role,
            ticket_information['description'],
            translation_provider.get_destination_language()
        )
    )
    code = trello_provider.add_comment_to_card(ticket_information['id'], chat_gpt_response)

    if (code == 200):
        updated_message = get_translated_message('TICKET_UPDATED')
        client.chat_postMessage(channel=channel_id, text=f"{updated_message} {ticket_information['name']} :white_check_mark:")
    else:
        client.chat_postMessage(channel=channel_id,
            blocks=[
                {'type': 'divider'},
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f"*I've failed to update ticket {ticket_information['name']}* but here are my thoughts for this: \n{chat_gpt_response.replace('**', '*')}"
                    }
                },
                {'type': 'divider'},
            ]
        )



# TODO add validation and maybe some abstraction for this complex route
def handle_ticket_command(**payload):
    # destructuring stuff
    channel_id, user_id, board = payload.get('channel_id'), payload.get('user_id'), payload.get('text')

    # check for valid board
    if board == '' or not any(list['name'] == board for list in lists):
        error_message = get_translated_message('NOT_BOARD_ERROR')
        client.chat_postMessage(channel=channel_id, board=error_message)
        return response(), 500
    
    # get user email via slack
    user_email = slack.get_user_email(user_id=user_id)

    # get translated searching message
    searching_message = get_translated_message('SEARCHING_TICKETS_MESSAGE')
    searching_message = searching_message.replace('{user_email}', user_email).replace('{board}', board)

    # send searching message
    client.chat_postMessage(channel=channel_id, text=searching_message)

    # get list_id
    list_id = list(filter(lambda list: (list['name'] == board), lists))[0]['list_id']

    # get user details
    user_details = trello_provider.get_member_details(user_email)

    # get tickets assigned per board
    tickets = trello_provider.get_tickets_by_asignee(list_id=list_id, member_id=user_details['id'])
    
    # get translated assigned tickets message
    assigned_tickets_message = get_translated_message('ASSIGNED_TICKETS_MESSAGE')
    assigned_tickets_message = assigned_tickets_message.replace('{user_email}', user_email).replace('{board}', board)

    # send back assigned tickets
    client.chat_postMessage(channel=channel_id, text= f'{assigned_tickets_message}\n' + ', \n'.join(tickets))

if __name__ == "__main__":
    app.run(debug=True)