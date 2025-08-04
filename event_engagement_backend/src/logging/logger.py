"""
Logger setup for the event engagement microservice.
"""
import logging

# PUBLIC_INTERFACE
def get_logger(name: str = "event_engagement_backend"):
    """
    Standard method to obtain a logger instance for the backend service.

    Args:
        name (str): Logger name.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
