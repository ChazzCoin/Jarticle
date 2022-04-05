from pathlib import Path
from dotenv import load_dotenv
import os
from Config import config
load_dotenv()

def get_env(key):
    if config.LOG_LEVEL >= config.VERBOSE:
        print(f"VERBOSE: Config.env -> Grabbing .env Variable for Key={key}, Value={os.environ.get(key)}")
    if key == "TIFFANY_BOT_PATH":
        temp = os.environ.get(key)
        if not temp or temp == "CWD":
            return get_parent_directory()
    return os.environ.get(key)

def get_parent_directory():
    path = Path(os.getcwd())
    return path.parent.absolute().__str__()
