# bots/run_xbot.py

import logging
from utils.logger_config import setup_logging
from bots.xbot import XBot

def main():
    setup_logging()
    bot = XBot()
    bot.ingest_data()

    # Example interaction
    user_query = "Can you explain the basics of Quantum Computing?"
    response = bot.process_query(user_query)
    print(f"Bot Response: {response}")

if __name__ == "__main__":
    main()
