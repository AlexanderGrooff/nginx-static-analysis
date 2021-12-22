import sys

from loguru import logger


def setup_logger(verbose: bool):
    log_level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level, format="{message}")
