# bots/xbot.py

import logging
import json
from utils.config import Config
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings
from utils.openai_utils import OpenAILLM
from utils.twitter_utils import TwitterAPI
from utils.memory import Memory
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from threading import Lock
import time

logger = logging.getLogger(__name__)

class XBot:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Implement singleton pattern to ensure only one instance of XBot exists.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(XBot, cls).__new__(cls)
        return cls._instance

    def __init__(self, character_config_path=None):
        """
        Initialize the XBot with all necessary utilities and character configuration.
        """
        if hasattr(self, '_initialized') and self._initialized:
            return  # Avoid re-initialization in singleton

        self.config = Config()
        self.character_config_path = character_config_path or self.config.character_config_path
        self.load_character_config(self.character_config_path)
        self.db_utils = LanceDBUtils(db_path=self.config.db_path)
        self.embedding_fn = LocalEmbeddings(model_name=self.config.embedding_model)
        self.memory = Memory(db_utils=self.db_utils, embedding_fn=self.embedding_fn)
        self.memory.set_character_name(self.character.get('name', 'Alexandra'))
        self.openai_llm = OpenAILLM(
            model=self.config.llm_model,
            llm_settings=self.character.get('llm_settings', {}),
            character_profile=self.character
        )
        self.twitter = TwitterAPI()
        self.interaction_policies = self.character.get('interaction_policies', {})
        self.rate_limit = self.interaction_policies.get('rate_limit_per_minute', 60)
        self.error_handling_strategy = self.interaction_policies.get('error_handling_strategy', 'retry_with_exponential_backoff')
        self.logging_level = self.interaction_policies.get('logging_level', 'INFO')
        self.last_tweet_time = 0
        self.tweet_interval = 60 / self.rate_limit if self.rate_limit > 0 else 0

        self._initialized = True
        logger.info("XBot initialized successfully.")

    def load_character_config(self, character_config_path):
        """
        Load the character configuration from a JSON file.

        :param character_config_path: Path to the character JSON file.
        """
        try:
            with open(character_config_path, 'r') as file:
                self.character = json.load(file)
            logger.info(f"Loaded character configuration from {character_config_path}.")
        except Exception as e:
            logger.error(f"Failed to load character configuration: {e}")
            self.character = {}

    def ingest_data(self):
        """
        Ingest data from URLs specified in the character configuration into LanceDB.
        """
        urls = self.character.get('ingestion_urls', [])
        if not urls:
            logger.warning("No ingestion URLs found in character configuration.")
            return

        logger.info("Ingesting data...")
        self.db_utils.create_table('xbot_data')
        try:
            self.db_utils.table.delete()  # Clear existing data
            logger.debug("Cleared existing data in the table.")
        except Exception as e:
            logger.warning(f"Could not clear table data: {e}")

        # Load and process data
        loader = UnstructuredURLLoader(urls=urls)
        documents = loader.load()
        logger.debug(f"Loaded {len(documents)} documents from URLs.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)
        logger.debug(f"Split documents into {len(docs)} chunks.")

        data = [
            {
                'id': idx,
                'text': doc.page_content,
                'source': doc.metadata.get('source', 'unknown')
            }
            for idx, doc in enumerate(docs)
        ]

        self.db_utils.add_data(data, embedding_fn=self.embedding_fn)
        logger.info("Data ingestion completed.")

    def generate_prompt(self, user_query):
        """
        Generate a prompt based on user query, conversation history, and character configuration.

        :param user_query: The user's query string.
        :return: The generated prompt string.
        """
        context = self.get_context_for_query(user_query)
        conversation_history = self.memory.get_recent_interactions(top_k=5)
        system_prompt = self.openai_llm.generate_system_prompt()
        full_prompt = f"{conversation_history}{context}\n\nUser's question: {user_query}\n{self.character.get('name', 'Alexandra')}'s answer:"
        return full_prompt

    def get_context_for_query(self, user_query):
        """
        Retrieve relevant context from the database based on the user query.

        :param user_query: The user's query string.
        :return: Concatenated relevant text snippets.
        """
        relevant_texts = self.db_utils.retrieve_relevant_info(
            query_text=user_query,
            embedding_fn=self.embedding_fn,
            top_k=3
        )

        if not relevant_texts:
            logger.warning("No relevant information found in the database.")
            return "I couldn't find any relevant information on that topic."

        return '\n'.join(relevant_texts)

    def process_query(self, user_query, recipient_screen_name=None):
        """
        Process a user query, generate a response, and post it as a tweet or send as a DM.

        :param user_query: The user's query string.
        :param recipient_screen_name: Optional Twitter handle to send a DM.
        :return: The generated response.
        """
        logger.info(f"Processing query: {user_query}")
        prompt = self.generate_prompt(user_query)

        response = self.openai_llm.generate_response(
            user_query=prompt
        )

        # Save interaction to memory
        self.memory.add_interaction(user_query, response)

        # Rate limiting
        current_time = time.time()
        if self.tweet_interval > 0:
            elapsed = current_time - self.last_tweet_time
            if elapsed < self.tweet_interval:
                sleep_time = self.tweet_interval - elapsed
                logger.debug(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds.")
                time.sleep(sleep_time)

        # Decide whether to post a tweet or send a DM
        if recipient_screen_name:
            recipient_id = self.twitter.get_user_id(recipient_screen_name)
            if recipient_id:
                self.twitter.send_direct_message(recipient_id, response)
                logger.info(f"Sent DM to @{recipient_screen_name}: {response}")
        else:
            tweets = self.split_text_for_twitter(response)
            for tweet_part in tweets:
                self.twitter.post_tweet(tweet_part)
                logger.info(f"Posted tweet: {tweet_part}")

        self.last_tweet_time = time.time()
        return response

    def split_text_for_twitter(self, text, character_limit=280):
        """
        Split text into chunks suitable for tweeting.

        :param text: The text to split.
        :param character_limit: Maximum number of characters per tweet.
        :return: List of text chunks.
        """
        response_format = self.character.get('response_format', {})
        use_emojis = response_format.get('use_emojis', False)
        include_hashtags = response_format.get('include_hashtags', False)
        include_mentions = response_format.get('include_mentions', False)

        hashtags = ''
        if include_hashtags:
            preferred_topics = self.character.get('preferred_topics', [])
            hashtags = ' '.join([f"#{topic.replace(' ', '')}" for topic in preferred_topics])

        mentions = ''
        if include_mentions:
            mentions = '@'  # Placeholder for mentions if needed

        prefix = ''
        if use_emojis:
            prefix = '😊 '

        words = text.split()
        chunks = []
        chunk = prefix

        for word in words:
            # Check if adding the next word exceeds the character limit
            potential_length = len(chunk) + len(word) + 1 + len(hashtags) + len(mentions)
            if potential_length <= character_limit:
                chunk += (' ' if len(chunk.strip()) > 0 else '') + word
            else:
                if hashtags and len(chunk) + len(hashtags) + len(mentions) + 1 <= character_limit:
                    chunk += f" {hashtags}"
                if mentions and len(chunk) + len(mentions) + 1 <= character_limit:
                    chunk += f" {mentions}"
                chunks.append(chunk)
                chunk = prefix + word

        if chunk:
            if hashtags and len(chunk) + len(hashtags) + len(mentions) + 1 <= character_limit:
                chunk += f" {hashtags}"
            if mentions and len(chunk) + len(mentions) + 1 <= character_limit:
                chunk += f" {mentions}"
            chunks.append(chunk)

        return chunks
