import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self._validate_env_vars()

        # OpenAI
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

        # Twitter
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET_KEY')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        # Database
        self.db_path = os.getenv('DB_PATH', 'my_lancedb')

        # Model configs
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
        self.llm_model = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')

    def _validate_env_vars(self):
        required_vars = [
            'OPENAI_API_KEY',
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET_KEY',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET'
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
