# utils/twitter_utils.py

import tweepy
import logging
from utils.config import Config

logger = logging.getLogger(__name__)

class TwitterAPI:
    def __init__(self):
        config = Config()
        self.api_key = config.twitter_api_key
        self.api_secret = config.twitter_api_secret
        self.access_token = config.twitter_access_token
        self.access_token_secret = config.twitter_access_token_secret

        try:
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api = tweepy.API(auth)
            logger.info("Authenticated with Twitter API.")
        except Exception as e:
            logger.error(f"Failed to authenticate with Twitter API: {e}")
            raise

    def get_user_id(self, screen_name):
        """
        Retrieve the user ID based on the Twitter screen name.

        :param screen_name: Twitter user's screen name.
        :return: User ID as a string.
        """
        try:
            user = self.api.get_user(screen_name=screen_name)
            logger.debug(f"Retrieved user ID for {screen_name}: {user.id}")
            return user.id_str
        except Exception as e:
            logger.error(f"Error retrieving user ID for {screen_name}: {e}")
            return None

    def send_direct_message(self, recipient_id, message):
        """
        Send a direct message to a Twitter user.

        :param recipient_id: The recipient's Twitter user ID.
        :param message: The message content.
        """
        try:
            self.api.send_direct_message(recipient_id, message)
            logger.info(f"Sent DM to user ID {recipient_id}.")
        except Exception as e:
            logger.error(f"Failed to send DM to user ID {recipient_id}: {e}")
