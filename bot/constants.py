from yaml import load, SafeLoader
from os import getenv
from dotenv import load_dotenv

with open("config.yaml", 'r') as file:
    _CONFIGURATION = load(file, Loader=SafeLoader)

def get_values(major: str) -> dict:
    return _CONFIGURATION[major]

class Colour:
    _ = get_values('style')
    EXCEPTION = _['exception']
    SUNSHINE = _['sunshine']
    DEEPBLUE = _['deepblue']

class Defaults:
    _ = get_values('bot')
    PREFIX = _['prefix']

class Admins:
    ID_LIST = get_values('bot')['admins']

class Props:
    _ = get_values('props')
    CHARACTER_URL = _['character']
    HELP_BOARD = _['help_board']
    HELP_DESCRIPTION = _['help_desc']

class Tokens:
    load_dotenv()
    DISCORD_TOKEN = getenv('TOKEN')
    GITHUB_TOKEN = getenv('GITHUB')
    