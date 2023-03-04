import requests
import os

class Trello:
    def __init__(self):
        self.board_id = '632eb65e083d900016aa87dd'
        self.trello_token = os.environ['trello_token']
        self.trello_api_key = os.environ['trello_api_key']
    def authenticated_request(self, url):
        return requests.get(f'{url}?key={self.trello_api_key}&token={self.trello_token}')

    def get_all_lists(self):
        r = self.authenticated_request(f'https://api.trello.com/1/boards/{self.board_id}/lists')
        lists = r.json()
        to_return = []
        for list in lists:
            to_return.append(list.get('name'))
        return " , ".join(to_return)
        