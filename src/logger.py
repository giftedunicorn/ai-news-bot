"""
Logging configuration for the AI News Bot
"""
import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: str = "INFO",
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with the specified configuration.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper()))

        # Default format if none provided
        if log_format is None:
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
