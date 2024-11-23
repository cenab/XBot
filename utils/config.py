# utils/config.py

import os
from dotenv import load_dotenv
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__init_config()
        return cls._instance

    def __init_config(self):
        load_dotenv()
        self._validate_env_vars()

        # OpenAI
        self.openai_api_key: str = os.getenv('OPENAI_API_KEY')

        # Twitter
        self.twitter_api_key: str = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret: str = os.getenv('TWITTER_API_SECRET_KEY')
        self.twitter_access_token: str = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret: str = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        # Database
        self.db_path: str = os.getenv('DB_PATH', 'my_lancedb')

        # Model configs
        self.embedding_model: str = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
        self.llm_model: str = os.getenv('LLM_MODEL', 'gpt-4')  # Updated to GPT-4

        # Character configuration
        self.character_config_path: str = os.getenv('CHARACTER_CONFIG_PATH', 'config/xbot_character.json')

    def _validate_env_vars(self) -> None:
        required_vars = [
            'OPENAI_API_KEY',
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET_KEY',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET',
            'CHARACTER_CONFIG_PATH'
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}. Please set them in the .env file.")
