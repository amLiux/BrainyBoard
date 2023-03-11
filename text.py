from googletrans import Translator, constants
import os

MESSAGES = {
    'WELCOME_MESSAGE': (
        'Welcome to the {change_channel} channel! \n\n'
        'Finish the following tasks to get started!'
    ),
    'NOT_BOARD_ERROR': (
        'Please provide a board e.g: /tickets <boardToLookup>'
    ),
    'SEARCHING_TICKETS_MESSAGE': (
        'Looking tickets assigned to: {user_email} in board: {board}'
    ),
    'LISTS_MESSAGE': 'Lists in your board:',
    'REACT_MESSAGE': 'React to this message! And complete the following tasks: \n',
    'ASSIGNED_TICKETS_MESSAGE': (
        'Tickets assigned to: {user_email} in {board}:'
    ),
    'TICKET_UPDATED': "*I've updated your ticket*:",
    'THINKING_MESSAGE': "*I'm thinking*, this might take a second :clock1:"
}

class TranslationProvider:
    def __init__(self):
        self.google_service = Translator()
        self.destination_language = os.environ['destination_language']

    def translate(self, key):
        t = self.google_service.translate(MESSAGES[key], dest=self.destination_language)
        return t.text

    def get_destination_language(self):
        return self.destination_language
    

