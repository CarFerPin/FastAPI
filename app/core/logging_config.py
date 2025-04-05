import logging
from fastapi import Request
from datetime import datetime

# Configure the general logger
app_logger = logging.getLogger("app_logger")
app_logger.setLevel(logging.INFO)

# Configure the log file for app.log
app_handler = logging.FileHandler("app.log")
app_handler.setLevel(logging.INFO)

# Define the log format
app_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
app_handler.setFormatter(app_formatter)

# Add the handler to the logger
app_logger.addHandler(app_handler)

async def log_request_response(request: Request, call_next):
    """
    Middleware to log incoming requests and outgoing responses.

    Args:
        request (Request): The incoming HTTP request.
        call_next (function): The next middleware or route handler.

    Returns:
        Response: The processed HTTP response.
    """
    # Log the incoming request
    app_logger.info(f"Request: {request.method} {request.url}")
    app_logger.info(f"Headers: {dict(request.headers)}")
    if request.method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        body = await request.body()
        app_logger.info(f"Body: {body.decode('utf-8')}")

    # Process the response
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()

    # Log the response
    app_logger.info(f"Response status: {response.status_code}")
    app_logger.info(f"Process time: {process_time} seconds")
    return response

def log_error(error: Exception):
    """
    Log an error.

    Args:
        error (Exception): The exception to log.
    """
    app_logger.error(f"Error: {error}")