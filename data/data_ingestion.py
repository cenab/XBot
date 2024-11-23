# data/data_ingestion.py

import logging
import argparse
from utils.logger_config import setup_logging
from bots.xbot import XBot

def ingest_data(config_path: str, table_name: str) -> None:
    """
    Ingest data into the database using the XBot class.

    :param config_path: Path to the character configuration JSON file.
    :param table_name: Name of the database table to use.
    """
    try:
        bot = XBot(config_path=config_path, table_name=table_name)
        bot.ingest_data()
    except Exception as e:
        logging.error(f"Error during data ingestion: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data for XBot.")
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
    setup_logging()
    ingest_data(config_path=args.config_path, table_name=args.table_name)
