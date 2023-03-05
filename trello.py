import requests
import os

class Trello:
    def __init__(self):
        self.board_id = os.environ['board_id']
        self.trello_token = os.environ['trello_token']
        self.trello_api_key = os.environ['trello_api_key']
        self.lists = self._get_all_lists()
    def authenticated_request(self, url):
        return requests.get(f'{url}?key={self.trello_api_key}&token={self.trello_token}')

    def _get_all_lists(self):
        r = self.authenticated_request(f'https://api.trello.com/1/boards/{self.board_id}/lists')
        lists = r.json()
        to_return = []
        for list in lists:
            to_return.append({'name': list.get('name'), 'list_id': list.get('id')})
        return to_return
    
    def get_tickets_by_asignee(self, list_id):
        r = self.authenticated_request(f'https://api.trello.com/1/lists/{list_id}/cards')
        cards = r.json()
        to_return = []
        for card in cards:
            to_return.append(card.get('name'))
        return " , ".join(to_return)
