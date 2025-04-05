import logging

# Configure the logger for database operations
db_logger = logging.getLogger("db_logger")
db_logger.setLevel(logging.INFO)

# Configure the log file for database changes
db_handler = logging.FileHandler("db_changes.log")
db_handler.setLevel(logging.INFO)

# Define the log format
db_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
db_handler.setFormatter(db_formatter)

# Add the handler to the logger
db_logger.addHandler(db_handler)

def log_db_change(action: str, details: str):
    """
    Log a database operation.

    Args:
        action (str): The action performed (e.g., CREATE, UPDATE, DELETE).
        details (str): Details about the operation.

    Example:
        log_db_change("CREATE", "Created a new user with ID 12345")
    """
    db_logger.info(f"Action: {action} - Details: {details}")