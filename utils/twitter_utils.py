# twitter_utils.py

import logging
import sys
import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('twitter_send_message.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def create_api():
    """
    Creates and returns a Tweepy API object after authenticating with Twitter.
    """
    # Load credentials from environment variables
    API_KEY = os.getenv('API_KEY')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    try:
        auth = tweepy.OAuth1UserHandler(
            API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)
        logger.debug('Twitter API authentication successful.')
        return api
    except tweepy.TweepyException as e:
        logger.error(f'Authentication failed: {e}')
        sys.exit(1)

def send_direct_message(api, recipient_id, text):
    """
    Sends a direct message to the specified user ID.

    Parameters:
    - api: Authenticated Tweepy API object.
    - recipient_id: The user ID of the recipient.
    - text: The message text to send.
    """
    try:
        api.send_direct_message(recipient_id=recipient_id, text=text)
        logger.info(f'Message sent to user ID {recipient_id}.')
    except tweepy.TweepyException as e:
        logger.error(f'Failed to send message: {e}')
        sys.exit(1)

def get_user_id(api, screen_name):
    """
    Retrieves the user ID for a given screen name.

    Parameters:
    - api: Authenticated Tweepy API object.
    - screen_name: The screen name of the user.

    Returns:
    - The user ID as a string.
    """
    try:
        user = api.get_user(screen_name=screen_name)
        user_id = user.id_str
        logger.debug(f'User ID for {screen_name} is {user_id}.')
        return user_id
    except tweepy.TweepyException as e:
        logger.error(f'Failed to retrieve user ID: {e}')
        sys.exit(1)
