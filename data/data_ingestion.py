import logging
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def ingest_data(urls, db_path='my_lancedb', table_name='my_table', embedding_model='sentence-transformers/all-MiniLM-L6-v2'):
    """
    Ingest data from specified URLs and add to LanceDB.

    :param urls: List of URLs to fetch data from.
    :param db_path: Path to the LanceDB database.
    :param table_name: Name of the table in LanceDB.
    :param embedding_model: Model name for generating embeddings.
    """
    logger.info("Starting data ingestion process.")

    # Initialize LanceDB utilities
    db_utils = LanceDBUtils(db_path=db_path)
    table = db_utils.create_table(table_name)

    # Clear existing data in the table (use with caution)
    try:
        table.delete()  # Assuming LanceDB has a delete method to clear table data
        logger.debug("Cleared existing data in the table.")
    except Exception as e:
        logger.warning(f"Could not clear table data: {e}")

    # Initialize the local embedding function
    embedding_fn = LocalEmbeddings(model_name=embedding_model)

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
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning",
        # Add more URLs as needed
    ]
    ingest_data(urls)
