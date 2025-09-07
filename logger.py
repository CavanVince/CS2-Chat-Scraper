import logging
import sys

_root_handler_setup = False

def setup_logging(log_level=logging.INFO):
    """Set up logging configuration for the entire application"""
    global _root_handler_setup
    
    if _root_handler_setup:
        return
    
    # Configure the actual root logger (empty string name)
    # This ensures ALL loggers inherit the handler
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s - %(name)s - %(levelname)s]: %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(handler)
    
    _root_handler_setup = True

def get_logger(name: str = None, log_level: int = logging.INFO) -> logging.Logger:
    """Get a logger, typically called with __name__"""
    # Ensure logging is configured
    setup_logging()
    
    # Use the provided name or default to app
    logger_name = name if name else "app"
    logger = logging.getLogger(logger_name)
    
    if log_level is not None:
        logger.setLevel(log_level)
    
    return logger