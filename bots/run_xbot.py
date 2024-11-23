# bots/run_xbot.py

import logging
import argparse
from utils.logger_config import setup_logging
from bots.xbot import XBot

def main(config_path: str, table_name: str):
    try:
        setup_logging()
        bot = XBot(config_path=config_path, table_name=table_name)
        bot.ingest_data()

        # Example interaction
        user_query = "Can you explain the basics of Quantum Computing?"
        response = bot.process_query(user_query)
        print(f"Bot Response: {response}")
    except Exception as e:
        logging.error(f"An error occurred in main: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the XBot.")
    parser.add_argument(
        '--config_path',
        type=str,
        default='config/xbot_character.json',
        help='Path to the character configuration JSON file.'
    )
    parser.add_argument(
        '--table_name',
        type=str,
        default='xbot_data',
        help='Name of the database table to use.'
    )
    args = parser.parse_args()
    main(config_path=args.config_path, table_name=args.table_name)
