import logging
from utils.config import Config
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings
from utils.openai_utils import OpenAILLM
from utils.twitter_utils import TwitterAPI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class XBot:
    def __init__(self):
        """
        Initialize the XBot with all necessary utilities.
        """
        self.config = Config()
        self.db_utils = LanceDBUtils(db_path=self.config.db_path)
        self.embedding_fn = LocalEmbeddings(model_name=self.config.embedding_model)
        self.openai_llm = OpenAILLM(model=self.config.llm_model)
        self.twitter = TwitterAPI()

    def ingest_data(self, urls):
        """
        Ingest data from specified URLs into LanceDB.

        :param urls: List of URLs to fetch data from.
        """
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

    def process_query(self, user_query):
        """
        Process a user query, generate a response, and post it as a tweet.

        :param user_query: The user's query string.
        :return: The generated response.
        """
        logger.info(f"Processing query: {user_query}")
        relevant_texts = self.db_utils.retrieve_relevant_info(
            query_text=user_query,
            embedding_fn=self.embedding_fn,
            top_k=3
        )

        if not relevant_texts:
            logger.warning("No relevant information found in the database.")
            return "No relevant information found in the database."

        context = '\n'.join(relevant_texts)
        system_prompt = "You are a helpful assistant. Use the following context to answer the user's question."
        full_prompt = f"{context}\n\nUser's question: {user_query}\nAnswer:"

        response = self.openai_llm.generate_response(
            prompt=full_prompt,
            system_prompt=system_prompt
        )

        # Post the response as a tweet
        self.twitter.post_tweet(response)
        logger.info("Response posted as a tweet.")
        return response
