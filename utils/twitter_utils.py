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

    def post_tweet(self, message):
        """
        Post a tweet with the given message.

        :param message: The content of the tweet.
        """
        try:
            self.api.update_status(status=message)
            logger.info("Tweet posted successfully.")
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
