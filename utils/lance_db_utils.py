import lancedb
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class LanceDBUtils:
    def __init__(self, db_path):
        """
        Initialize the LanceDB connection.

        :param db_path: The directory path where the database is stored.
        """
        self.db = lancedb.connect(db_path)
        self.table = None

    def create_table(self, table_name):
        """
        Create a new table in the database or open it if it already exists.

        :param table_name: Name of the table to create or open.
        :return: The table object.
        """
        if table_name not in self.db.table_names():
            self.table = self.db.create_table(table_name)
            logger.info(f"Created new table: {table_name}")
        else:
            self.table = self.db.open_table(table_name)
            logger.info(f"Opened existing table: {table_name}")
        return self.table

    def add_data(self, data, embedding_fn=None):
        """
        Add data to the table.

        :param data: Data to add (list of dicts or Pandas DataFrame).
        :param embedding_fn: Optional embedding function to generate embeddings.
        """
        if not self.table:
            raise ValueError("Table is not initialized. Call create_table() first.")
        try:
            if embedding_fn:
                self.table.add(data, embedding=embedding_fn)
                logger.debug("Added data with embeddings.")
            else:
                self.table.add(data)
                logger.debug("Added data without embeddings.")
        except Exception as e:
            logger.error(f"Failed to add data to table: {e}")
            raise

    def retrieve_relevant_info(self, query_text, embedding_fn, top_k=5):
        """
        Retrieve relevant information from LanceDB based on a query text.

        :param query_text: The user's query text.
        :param embedding_fn: Embedding function to generate the query embedding.
        :param top_k: Number of relevant results to retrieve.
        :return: List of relevant text snippets.
        """
        try:
            query_embedding = embedding_fn([query_text])[0]
            results = self.table.search(query_embedding).limit(top_k).to_df()
            relevant_texts = results['text'].tolist()
            logger.debug(f"Retrieved {len(relevant_texts)} relevant texts.")
            return relevant_texts
        except Exception as e:
            logger.error(f"Error retrieving relevant information: {e}")
            return []

class LocalEmbeddings:
    def __init__(self, model_name):
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

    def __call__(self, texts):
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
