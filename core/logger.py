"""
Shared logging utilities for ReliabilityPlatform.
"""

import logging

LOGGER_NAME = "ReliabilityPlatform"


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a configured logger.

    Examples:
        logger = get_logger()
        logger = get_logger("incident_commander")
    """

    logger_name = LOGGER_NAME

    if name:
        logger_name = f"{LOGGER_NAME}.{name}"

    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger