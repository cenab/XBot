# data/data_ingestion.py

import logging
import json
from utils.config import Config
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def ingest_data(character_config_path='config/xbot_character.json'):
    """
    Ingest data from URLs specified in the character configuration and add to LanceDB.

    :param character_config_path: Path to the character JSON file containing ingestion URLs.
    """
    logger.info("Starting data ingestion process.")

    # Load character configuration
    try:
        with open(character_config_path, 'r') as file:
            character = json.load(file)
        logger.info(f"Loaded character configuration from {character_config_path}.")
    except Exception as e:
        logger.error(f"Failed to load character configuration: {e}")
        return

    urls = character.get('ingestion_urls', [])
    if not urls:
        logger.warning("No ingestion URLs found in character configuration.")
        return

    # Initialize LanceDB utilities
    config = Config()
    db_utils = LanceDBUtils(db_path=config.db_path)
    table = db_utils.create_table('my_table')

    # Clear existing data in the table (use with caution)
    try:
        table.delete()  # Assuming LanceDB has a delete method to clear table data
        logger.debug("Cleared existing data in the table.")
    except Exception as e:
        logger.warning(f"Could not clear table data: {e}")

    # Initialize the local embedding function
    embedding_fn = LocalEmbeddings(model_name=config.embedding_model)

    # Load documents from URLs
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()
    logger.debug(f"Loaded {len(documents)} documents from URLs.")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    logger.debug(f"Split documents into {len(docs)} chunks.")

    # Prepare data to insert into LanceDB
    data = [
        {
            'id': idx,
            'text': doc.page_content,
            'source': doc.metadata.get('source', 'unknown')
        }
        for idx, doc in enumerate(docs)
    ]

    # Add data with embeddings
    db_utils.add_data(data, embedding_fn=embedding_fn)
    logger.info("Data ingestion completed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    ingest_data()
