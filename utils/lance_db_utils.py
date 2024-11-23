# utils/lance_db_utils.py

import lancedb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)

class LanceDBUtils:
    def __init__(self, db_path: str):
        """
        Initialize the LanceDB connection.

        :param db_path: The directory path where the database is stored.
        """
        try:
            self.db = lancedb.connect(db_path)
            logger.info(f"Connected to LanceDB at {db_path}.")
            self.table = None
        except Exception as e:
            logger.error(f"Failed to connect to LanceDB at {db_path}: {e}")
            raise

    def create_table(self, table_name: str) -> Any:
        """
        Create a new table in the database or open it if it already exists.

        :param table_name: Name of the table to create or open.
        :return: The table object.
        """
        try:
            if table_name not in self.db.table_names():
                self.table = self.db.create_table(table_name)
                logger.info(f"Created new table: {table_name}")
            else:
                self.table = self.db.open_table(table_name)
                logger.info(f"Opened existing table: {table_name}")
            return self.table
        except Exception as e:
            logger.error(f"Error creating or opening table '{table_name}': {e}")
            raise

    def clear_table(self, table_name: str) -> None:
        """
        Clear all data from the specified table.

        :param table_name: Name of the table to clear.
        """
        try:
            table = self.create_table(table_name)
            table.delete()  # Assuming LanceDB has a delete method to clear table data
            logger.debug(f"Cleared all data from table '{table_name}'.")
        except Exception as e:
            logger.warning(f"Could not clear table '{table_name}' data: {e}")

    def add_data(self, data: List[Dict[str, Any]], embedding_fn: Optional[Callable[[List[str]], List[List[float]]]] = None) -> None:
        """
        Add data to the table.

        :param data: Data to add (list of dicts).
        :param embedding_fn: Optional embedding function to generate embeddings.
        """
        if not self.table:
            raise ValueError("Table is not initialized. Call create_table() first.")
        try:
            if embedding_fn:
                texts = [item['text'] for item in data]
                embeddings = embedding_fn(texts)
                for item, embedding in zip(data, embeddings):
                    item['embedding'] = embedding
            self.table.insert(data)
            logger.debug("Added data to table.")
        except Exception as e:
            logger.error(f"Failed to add data to table: {e}")
            raise

    def retrieve_relevant_info(self, query_text: str, embedding_fn: Callable[[List[str]], List[List[float]]], top_k: int = 5) -> List[str]:
        """
        Retrieve relevant information from LanceDB based on a query text.

        :param query_text: The user's query text.
        :param embedding_fn: Embedding function to generate the query embedding.
        :param top_k: Number of relevant results to retrieve.
        :return: List of relevant text snippets.
        """
        try:
            query_embedding = embedding_fn([query_text])[0]
            results = self.table.search(query_embedding, "embedding").limit(top_k).to_df()
            relevant_texts = results['text'].tolist()
            logger.debug(f"Retrieved {len(relevant_texts)} relevant texts for query '{query_text}'.")
            return relevant_texts
        except Exception as e:
            logger.error(f"Error retrieving relevant information: {e}")
            return []

class LocalEmbeddings:
    def __init__(self, model_name: str):
        """
        Initialize the local embedding model.

        :param model_name: Name of the embedding model to use.
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model '{model_name}': {e}")
            raise

    def __call__(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        :param texts: List of text strings.
        :return: List of embeddings.
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True).tolist()
            logger.debug(f"Generated embeddings for {len(texts)} texts.")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
