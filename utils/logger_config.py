# utils/logger_config.py

import logging
from typing import Optional

def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """
    Set up logging configuration.

    :param level: Logging level.
    :param log_file: Optional path to a log file.
    """
    handlers = [
        logging.StreamHandler()
    ]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
