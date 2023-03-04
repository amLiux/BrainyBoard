from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, request, Response

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
    def get_http_utils(self):
        d = dict()
        d['request'] = request
        d['response'] = Response
        return d