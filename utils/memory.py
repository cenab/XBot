# utils/memory.py

import logging
from datetime import datetime
from uuid import uuid4
from typing import List
from utils.lance_db_utils import LanceDBUtils, LocalEmbeddings

logger = logging.getLogger(__name__)

class Memory:
    def __init__(self, db_utils: LanceDBUtils, embedding_fn: LocalEmbeddings, table_name: str = 'conversation_memory', max_history: int = 50):
        """
        Initialize the Memory system using LanceDB.

        :param db_utils: Instance of LanceDBUtils for database operations.
        :param embedding_fn: Instance of LocalEmbeddings for generating embeddings.
        :param table_name: Name of the table to store conversation histories.
        :param max_history: Maximum number of interactions to retain.
        """
        self.db_utils = db_utils
        self.embedding_fn = embedding_fn
        self.table_name = table_name
        self.max_history = max_history
        self.table = self.db_utils.create_table(self.table_name)

    def set_character_name(self, name: str) -> None:
        """
        Set the character's name for personalized interactions.

        :param name: Character's name.
        """
        self.character_name = name

    def add_interaction(self, user_query: str, bot_response: str) -> None:
        """
        Add a user query and bot response to the memory.

        :param user_query: The user's input.
        :param bot_response: Alexandra's response.
        """
        try:
            interaction = {
                'id': str(uuid4()),
                'timestamp': datetime.utcnow().isoformat(),
                'user_query': user_query,
                'bot_response': bot_response
            }
            # Generate embedding based on the combined interaction
            combined_text = f"User: {user_query}\n{self.character_name}: {bot_response}"
            interaction['embedding'] = self.embedding_fn([combined_text])[0]

            self.db_utils.add_data([interaction], embedding_fn=None)  # Embedding already added
            logger.debug(f"Added interaction to memory: {interaction['id']}")

            # Prune memory if exceeding max_history
            self.prune_memory()
        except Exception as e:
            logger.error(f"Error adding interaction to memory: {e}")

    def prune_memory(self) -> None:
        """
        Ensure the memory does not exceed the maximum history limit.
        """
        try:
            df = self.table.to_df()
            total_interactions = len(df)
            if total_interactions > self.max_history:
                num_to_remove = total_interactions - self.max_history
                # Retrieve the oldest interactions
                oldest = df.sort_values(by='timestamp').head(num_to_remove)
                ids_to_remove = oldest['id'].tolist()
                self.table.delete(ids_to_remove)
                logger.debug(f"Pruned {num_to_remove} interactions from memory.")
        except Exception as e:
            logger.error(f"Error pruning memory: {e}")

    def get_recent_interactions(self, top_k: int = 5) -> str:
        """
        Retrieve the most recent interactions.

        :param top_k: Number of recent interactions to retrieve.
        :return: Concatenated string of recent interactions.
        """
        try:
            df = self.table.to_df().sort_values(by='timestamp', ascending=False).head(top_k)
            interactions = [f"User: {row['user_query']}\n{self.character_name}: {row['bot_response']}" for _, row in df.iterrows()]
            logger.debug(f"Retrieved {len(interactions)} recent interactions from memory.")
            return '\n'.join(interactions[::-1])  # Reverse to maintain chronological order
        except Exception as e:
            logger.error(f"Error retrieving recent interactions: {e}")
            return ""
