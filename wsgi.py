import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app
#62608713e67249a2bd61d07812046caf