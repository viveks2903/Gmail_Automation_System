import logging

# Set up logging
logging.basicConfig(filename='logs/email_processor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(message):
    """Log an informational message."""
    logging.info(message)

def log_error(message):
    """Log an error message."""
    logging.error(message)
