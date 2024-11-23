from utils.config import Config
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings, OpenAILLM
from utils.twitter_utils import TwitterAPI
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class XBot:
    def __init__(self):
        self.config = Config()
        self.db_utils = LanceDBUtils(db_path=self.config.db_path)
        self.embedding_fn = LocalEmbeddings(model_name=self.config.embedding_model)
        self.openai_llm = OpenAILLM(model=self.config.llm_model)
        self.twitter = TwitterAPI()
        
    def ingest_data(self, urls):
        table = self.db_utils.create_table('my_table')
        table.clear()
        
        loader = UnstructuredURLLoader(urls=urls)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)
        
        data = [
            {
                'id': idx,
                'text': doc.page_content,
                'source': doc.metadata.get('source', 'unknown')
            }
            for idx, doc in enumerate(docs)
        ]
        
        self.db_utils.add_data(data, embedding_fn=self.embedding_fn)
        
    def process_query(self, user_query, recipient_screen_name):
        relevant_texts = self.db_utils.retrieve_relevant_info(
            query_text=user_query,
            embedding_fn=self.embedding_fn,
            top_k=3
        )
        
        if not relevant_texts:
            return "No relevant information found in the database."
            
        context = '\n'.join(relevant_texts)
        system_prompt = "You are a helpful assistant. Use the following context to answer the user's question."
        full_prompt = f"{context}\n\nUser's question: {user_query}\nAnswer:"
        
        response = self.openai_llm.generate_response(
            prompt=full_prompt,
            system_prompt=system_prompt
        )
        
        recipient_id = self.twitter.get_user_id(recipient_screen_name)
        self.twitter.send_direct_message(recipient_id, response)
        
        return response
