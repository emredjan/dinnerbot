import os
from os.path import join, dirname
from dotenv import load_dotenv

# python-dotenv configuration
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# read secrets from environment variables
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = os.environ.get('BOT_ID')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# other constants
BOT_NAME = 'dinnerbot'