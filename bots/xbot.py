# bots/xbot.py

import logging
import json
import os
from utils.config import Config
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings
from utils.openai_utils import OpenAILLM
from utils.twitter_utils import TwitterAPI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class XBot:
    def __init__(self, character_config_path=None):
        """
        Initialize the XBot with all necessary utilities and character configuration.
        """
        self.config = Config()
        self.character_config_path = character_config_path or self.config.character_config_path
        self.load_character_config(self.character_config_path)
        self.db_utils = LanceDBUtils(db_path=self.config.db_path)
        self.embedding_fn = LocalEmbeddings(model_name=self.config.embedding_model)
        self.openai_llm = OpenAILLM(model=self.config.llm_model, llm_settings=self.character.get('llm_settings', {}))
        self.twitter = TwitterAPI()
        self.interaction_policies = self.character.get('interaction_policies', {})

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
        self.db_utils.create_table('my_table')
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
        Generate a prompt based on user query and character configuration.

        :param user_query: The user's query string.
        :return: The generated prompt string.
        """
        context = self.get_context_for_query(user_query)
        system_prompt = self.character.get('additional_instructions', "You are a helpful assistant.")
        communication_style = self.character.get('communication_style', '')
        full_prompt = f"{communication_style}\n\n{context}\n\nUser's question: {user_query}\nAnswer:"
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
            return "No relevant information found in the database."

        return '\n'.join(relevant_texts)

    def process_query(self, user_query):
        """
        Process a user query, generate a response, and post it as a tweet.

        :param user_query: The user's query string.
        :return: The generated response.
        """
        logger.info(f"Processing query: {user_query}")
        prompt = self.generate_prompt(user_query)

        response = self.openai_llm.generate_response(
            prompt=prompt,
            system_prompt=self.character.get('additional_instructions', None)
        )

        # Ensure response adheres to Twitter's character limit and formatting
        tweets = self.split_text_for_twitter(response)
        for tweet_part in tweets:
            self.twitter.post_tweet(tweet_part)
            logger.info(f"Posted tweet: {tweet_part}")

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

        words = text.split()
        chunks = []
        chunk = ''

        for word in words:
            # Check if adding the next word exceeds the character limit
            if len(chunk) + len(word) + 1 <= character_limit:
                chunk += (' ' if chunk else '') + word
            else:
                if chunk:
                    chunks.append(chunk)
                chunk = word

        if chunk:
            chunks.append(chunk)

        # Optionally add hashtags
        if include_hashtags:
            hashtags = ' '.join([f"#{topic.replace(' ', '')}" for topic in self.character.get('preferred_topics', [])])
            for i in range(len(chunks)):
                if len(chunks[i]) + len(hashtags) + 1 <= character_limit:
                    chunks[i] += f" {hashtags}"

        # Optionally add emojis
        if use_emojis:
            for i in range(len(chunks)):
                chunks[i] = f"😊 {chunks[i]}"

        return chunks
