from requests import get, post 
import os

method_dict = {
    'GET': get,
    'POST': post,
}

class Trello:
    def __init__(self):
        self.trello_api_url = 'https://api.trello.com/1'
        self.board_id = os.environ['board_id']
        self.trello_token = os.environ['trello_token']
        self.trello_api_key = os.environ['trello_api_key']
        self.lists = self._get_all_lists()
    def authenticated_request(self, url, method, params = None):
        request_with_method = method_dict[method]
        if params: return request_with_method(url, params={"key": self.trello_api_key, "token": self.trello_token, **params})
        return request_with_method(f'{url}?key={self.trello_api_key}&token={self.trello_token}')

    def _get_all_lists(self):
        r = self.authenticated_request(f'{self.trello_api_url}/boards/{self.board_id}/lists', 'GET')
        lists = r.json()
        to_return = []
        for list in lists:
            to_return.append({'name': list.get('name'), 'list_id': list.get('id')})
        return to_return
    
    def get_ticket_information(self, ticket_name):
        query = f'name:${ticket_name}'
        r = self.authenticated_request(f'{self.trello_api_url}/search', 'GET', params={"query": query, "modelTypes": "cards"})
        json_ticket_information = r.json()
        return {
            # TODO we can expand on this later if needed
            'description': json_ticket_information['cards'][0]['desc'],
            'id': json_ticket_information['cards'][0]['id'],
            'name': ticket_name
        }
    
    def get_member_details(self, member_email):
        r = self.authenticated_request(f'{self.trello_api_url}/members/{member_email}', 'GET')
        details = r.json()
        return {
            'id': details.get('id'),
            'username': details.get('username'),
            'email': member_email,
        }
    
    def add_comment_to_card(self, card_id, comment):
        r = self.authenticated_request(f'{self.trello_api_url}/cards/{card_id}/actions/comments', 'POST', {'text': comment})
        return r.status_code
        
    def get_tickets_by_asignee(self, list_id, member_id):
        r = self.authenticated_request(f'{self.trello_api_url}/lists/{list_id}/cards', 'GET')
        cards = r.json()
        to_return = []
        # getting the tickets that have matching member
        member_tickets = list(
            filter(
                lambda ticket: (member_id in ticket.get('idMembers')), 
                cards
            )
        )
        for ticket in member_tickets:
            to_return.append(ticket['name'])
        return to_return
