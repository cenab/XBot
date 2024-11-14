# data_ingestion.py

from lance_db_utils import LanceDBUtils, LocalEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def main():
    # Initialize the LanceDB utilities
    db_utils = LanceDBUtils(db_path='my_lancedb')
    
    # Create or open a table
    table = db_utils.create_table('my_table')
    
    # Initialize the local embedding function
    embedding_fn = LocalEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    
    # Define URLs to fetch information from
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning",
        # Add more URLs as needed
    ]
    
    # Use LangChain to load documents from URLs
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()
    
    # Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    # Prepare data to be inserted into LanceDB
    data = []
    for idx, doc in enumerate(docs):
        data.append({
            'id': idx,
            'text': doc.page_content,
            'source': doc.metadata.get('source', 'unknown')
        })
    
    # Add data with embeddings
    db_utils.add_data(data, embedding_fn=embedding_fn)
    
    print("Data has been added to LanceDB and is ready to be queried.")

if __name__ == '__main__':
    main()
