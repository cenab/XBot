# utils/memory.py

import logging
from datetime import datetime
from uuid import uuid4
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings

logger = logging.getLogger(__name__)

class Memory:
    def __init__(self, db_utils: LanceDBUtils, embedding_fn: LocalEmbeddings, table_name='conversation_memory', max_history=50):
        """
        Initialize the Memory system using LanceDB.

        :param db_utils: Instance of LanceDBUtils for database operations.
        :param embedding_fn: Instance of LocalEmbeddings for generating embeddings.
        :param table_name: Name of the table to store conversation histories.
        :param max_history: Maximum number of interactions to retain.
        """
        self.db_utils = db_utils
        self.embedding_fn = embedding_fn
        self.table = self.db_utils.create_table(table_name)
        self.max_history = max_history

    def add_interaction(self, user_query: str, bot_response: str):
        """
        Add a user query and bot response to the memory.

        :param user_query: The user's input.
        :param bot_response: Alexandra's response.
        """
        interaction = {
            'id': str(uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'user_query': user_query,
            'bot_response': bot_response
        }
        # Generate embedding based on the combined interaction
        combined_text = f"User: {user_query}\nAlexandra: {bot_response}"
        interaction['embedding'] = self.embedding_fn([combined_text])[0]

        self.db_utils.add_data([interaction], embedding_fn=None)  # Embedding already added
        logger.debug(f"Added interaction to memory: {interaction['id']}")

        # Prune memory if exceeding max_history
        self.prune_memory()

    def prune_memory(self):
        """
        Ensure the memory does not exceed the maximum history limit.
        """
        total_interactions = len(self.table.to_df())
        if total_interactions > self.max_history:
            # Calculate how many to remove
            num_to_remove = total_interactions - self.max_history
            # Retrieve the oldest interactions
            oldest = self.table.to_df().sort_values(by='timestamp').head(num_to_remove)
            for idx, row in oldest.iterrows():
                self.table.delete(row['id'])
                logger.debug(f"Pruned interaction from memory: {row['id']}")

    def get_recent_interactions(self, top_k=5):
        """
        Retrieve the most recent interactions.

        :param top_k: Number of recent interactions to retrieve.
        :return: List of interaction strings.
        """
        try:
            df = self.table.to_df().sort_values(by='timestamp', ascending=False).head(top_k)
            interactions = [f"User: {row['user_query']}\nAlexandra: {row['bot_response']}" for _, row in df.iterrows()]
            logger.debug(f"Retrieved {len(interactions)} recent interactions from memory.")
            return interactions[::-1]  # Reverse to maintain chronological order
        except Exception as e:
            logger.error(f"Error retrieving recent interactions: {e}")
            return []
