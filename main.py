import logging
from bots.xbot import XBot

def setup_logging():
    """
    Configure logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def main():
    """
    Main function to initialize the bot and process a sample query.
    """
    setup_logging()
    bot = XBot()

    # Example: Ingest data (you can modify or remove this as needed)
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning",
        # Add more URLs as needed
    ]
    bot.ingest_data(urls)

    # Example: Process a query
    user_query = "What are the main applications of artificial intelligence?"
    response = bot.process_query(user_query)
    print(f"Response: {response}")

if __name__ == "__main__":
        main()
