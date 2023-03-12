import os
import openai


class OpenAIProvider:
    def __init__(self):
        self.api_key = os.environ['openai_api_key']
        self.create_chat = openai.ChatCompletion.create
        openai.api_key = self.api_key
    def get_formatted_question(self, user_role, description, language):
        return "Hello ChatGPT, I'm a {user_role} working on a ticket that says: {description}, would you mind on giving me some guidance like links, code examples and such, please reply on markdown format but don't use headings, please reply back in the following language: {language} ".replace('{user_role}', user_role).replace('{description}', description).replace('{language}', language)
    def ask_chatgpt(self, message):
        r = self.create_chat( 
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return r.get('choices')[0]['message']['content']
