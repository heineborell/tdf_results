import logging


def setup_logger():
    """
    Sets up a logger to log messages both to the console and a file.

    Returns:
        logger (logging.Logger): Configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)  # Set the minimum logging level for the logger

    # Create a file handler to save logs to a file (mode='w' overwrites the file each time)
    file_handler = logging.FileHandler(
        "app.log", mode="w"
    )  # Overwrite the file each time
    file_handler.setLevel(logging.INFO)  # Log level for file handler

    # Create a stream handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Log level for console handler

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter(" %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
