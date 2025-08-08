import os
from log import logger
from dotenv import load_dotenv

load_dotenv(override=True)

# Check if the environment variables required are present or not?
# pull the environment variables
# get the value of the variables.

# Constants
REQ_ENV_VARIABLES = ['OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'GOOGLE_API_KEY']


class ParseLocalEnv:
    def __init__(self):
        self._verify_required_variables()

    def _verify_required_variables(self):
        for variable in REQ_ENV_VARIABLES:
            if not os.getenv(variable):
                logger.critical(f'Missing ENVIRONMENT value for "{variable}"')
    
    @classmethod
    def get_env_values(cls):
        cls()
        dict_env = {}
        for var_key in REQ_ENV_VARIABLES:
            if os.getenv(var_key):
                dict_env[var_key] = os.getenv(var_key)
            else:
                message = f'ENV Variable name provided is not correct or does not exist in your local ENV'
                logger.error(message)
                raise ValueError(message)
        return dict_env


