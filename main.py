# main.py

import logging
from bots.xbot import XBot

def setup_logging(level=logging.INFO):
    """
    Configure logging for the application.
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def main():
    """
    Main function to initialize the bot, ingest data, and process a sample query.
    """
    setup_logging()
    bot = XBot()

    # Ingest data from URLs specified in the character configuration
    bot.ingest_data()

    # Example: Process a query
    user_query = "What are the main applications of artificial intelligence?"
    response = bot.process_query(user_query)
    print(f"Response: {response}")

if __name__ == "__main__":
    main()
