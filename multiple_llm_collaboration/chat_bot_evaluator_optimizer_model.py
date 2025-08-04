from ..parse_env import ParseLocalEnv
from log import logger


class ChatBot:
    def __init__(self):
        self.google_api_key  = None
        self.open_ai_api_key = None
        self.loc_env = ParseLocalEnv.get_env_values()

    def get_api_keys(self):
        self.google_api_key = self.loc_env['Google_api_key']
        self.open_ai_api_key = self.loc_env['Openai_api_key']

    def setup_bot(self):
        message = ""