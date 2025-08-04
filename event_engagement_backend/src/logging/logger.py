"""
Logger setup for the event engagement microservice.

This utility provides a centralized, environment-driven logging configuration
for all modules and supports project-wide log levels and destinations.
Logs may be streamed or file-based, based on configuration.
"""
import logging
import os

# PUBLIC_INTERFACE
def get_logger(name: str = "event_engagement_backend"):
    """
    Standard method to obtain a logger instance for the backend service.

    Uses environment variables LOG_LEVEL (default: INFO), LOG_DESTINATION (default: "stdout"),
    and LOG_FILE (if LOG_DESTINATION=file).

    Args:
        name (str): Logger name.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    if not getattr(logger, "_configured", False):
        # Load configuration from environment
        level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_str, logging.INFO)

        destination = os.getenv("LOG_DESTINATION", "stdout").lower()
        logger.handlers.clear()  # Remove inherited/duplicate handlers
        
        if destination == "file":
            log_file = os.getenv("LOG_FILE", "service.log")
            handler = logging.FileHandler(log_file)
        else:
            handler = logging.StreamHandler()
        
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger._configured = True  # Prevent duplicate config
        logger.propagate = False   # Centralize logging
        logger.debug(f"Logger '{name}' configured (level={level_str}, dest={destination})")
    return logger
