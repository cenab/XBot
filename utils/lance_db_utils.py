# lance_db_utils.py

import lancedb
import pandas as pd
import numpy as np
from lancedb.embeddings import EmbeddingFunction
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv
import os

class LanceDBUtils:
    def __init__(self, db_path='lancedb_data'):
        """
        Initialize the LanceDB connection.

        :param db_path: The directory path where the database is stored.
        """
        self.db_path = db_path
        self.db = lancedb.connect(self.db_path)
        self.table = None

    def create_table(self, table_name):
        """
        Create a new table in the database or open it if it already exists.

        :param table_name: Name of the table to create or open.
        :return: The table object.
        """
        if table_name not in self.db.table_names():
            self.table = self.db.create_table(table_name)
        else:
            self.table = self.db.open_table(table_name)
        return self.table

    def add_data(self, data, embedding_fn=None):
        """
        Add data to the table.

        :param data: Data to add (list of dicts or Pandas DataFrame).
        :param embedding_fn: Optional embedding function to generate embeddings.
        """
        if self.table is None:
            raise ValueError("Table is not initialized. Call create_table() first.")
        if embedding_fn:
            self.table.add(data, embedding=embedding_fn)
        else:
            self.table.add(data)

    def query_data(self, query_filter=None):
        """
        Query data from the table.

        :param query_filter: Optional filter string for querying.
        :return: Pandas DataFrame of the query results.
        """
        if self.table is None:
            raise ValueError("Table is not initialized. Call create_table() first.")
        df = self.table.to_pandas()
        if query_filter:
            df = df.query(query_filter)
        return df

    def vector_search(self, query_vector, limit=5, query_filter=None):
        """
        Perform a vector similarity search.

        :param query_vector: The query vector for similarity search.
        :param limit: Number of results to return.
        :param query_filter: Optional filter string to combine with the search.
        :return: Pandas DataFrame of the search results.
        """
        if self.table is None:
            raise ValueError("Table is not initialized. Call create_table() first.")
        search = self.table.search(query_vector)
        if query_filter:
            search = search.where(query_filter)
        results = search.limit(limit).to_df()
        return results

    def retrieve_relevant_info(self, query_text, embedding_fn, top_k=5, query_filter=None):
        """
        Retrieve relevant information from LanceDB based on a query text.

        :param query_text: The user's query text.
        :param embedding_fn: Embedding function to generate the query embedding.
        :param top_k: Number of relevant results to retrieve.
        :param query_filter: Optional filter string to refine the search.
        :return: List of relevant text snippets.
        """
        query_embedding = embedding_fn([query_text])[0]
        results = self.vector_search(
            query_vector=query_embedding,
            limit=top_k,
            query_filter=query_filter
        )
        # Assuming the text field is named 'text'
        relevant_texts = results['text'].tolist()
        return relevant_texts

class LocalEmbeddings(EmbeddingFunction):
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize the local embedding model.

        :param model_name: Name of the embedding model to use.
        """
        self.model = SentenceTransformer(model_name)

    def __call__(self, texts):
        """
        Generate embeddings for a list of texts.

        :param texts: List of text strings.
        :return: List of embeddings.
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True).tolist()
        return embeddings

class OpenAILLM:
    def __init__(self, model='gpt-3.5-turbo'):
        """
        Initialize the OpenAI LLM.
        
        :param model: The OpenAI model to use.
        """
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.model = model
        openai.api_key = self.api_key

    def generate_response(self, prompt, system_prompt=None, max_tokens=150):
        """
        Generate a response from the OpenAI LLM.

        :param prompt: The user prompt to send to the LLM.
        :param system_prompt: Optional system prompt to set the assistant's behavior.
        :param max_tokens: Maximum number of tokens in the response.
        :return: The LLM's response text.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )

        return response['choices'][0]['message']['content']
