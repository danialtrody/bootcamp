import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

LOG_FORMAT = "%(asctime)s - %(levelname)s - [%(name)s] %(message)s"


def setup_logging(log_file_path: Optional[str] = None, max_bytes: int = 0) -> None:
    """Configure root logger with a stream handler and optional rotating file handler."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT)

    # Always log to the terminal (stderr)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Optionally also write to a rotating file
    if log_file_path:
        fh = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=5)
        fh.setFormatter(formatter)
        root_logger.addHandler(fh)
