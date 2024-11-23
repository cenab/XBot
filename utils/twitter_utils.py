# utils/twitter_utils.py

import tweepy
import logging
from utils.config import Config
import time

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
            self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            self.api.verify_credentials()
            logger.info("Authenticated with Twitter API.")
        except Exception as e:
            logger.error(f"Failed to authenticate with Twitter API: {e}")
            raise

    def post_tweet(self, message):
        """
        Post a tweet with the given message.

        :param message: The content of the tweet.
        """
        try:
            self.api.update_status(status=message)
            logger.info("Tweet posted successfully.")
        except tweepy.TweepError as e:
            logger.error(f"Failed to post tweet: {e}")
            # Implement retry logic or other error handling as needed
        except Exception as e:
            logger.error(f"An unexpected error occurred while posting tweet: {e}")

    def send_direct_message(self, user_id, message):
        """
        Send a direct message to a user.

        :param user_id: The Twitter user ID to send the DM to.
        :param message: The content of the DM.
        """
        try:
            self.api.send_direct_message(recipient_id=user_id, text=message)
            logger.info(f"Direct message sent to user ID {user_id}.")
        except tweepy.TweepError as e:
            logger.error(f"Failed to send direct message: {e}")
            # Implement retry logic or other error handling as needed
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending DM: {e}")

    def get_user_id(self, screen_name):
        """
        Retrieve the user ID for a given Twitter screen name.

        :param screen_name: The Twitter handle of the user.
        :return: The user ID or None if not found.
        """
        try:
            user = self.api.get_user(screen_name=screen_name)
            logger.debug(f"Retrieved user ID {user.id} for screen name '{screen_name}'.")
            return user.id
        except tweepy.TweepError as e:
            logger.error(f"Failed to retrieve user ID for '{screen_name}': {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while retrieving user ID: {e}")
            return None
