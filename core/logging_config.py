from __future__ import annotations
import logging
from pathlib import Path
from config.settings import LOG_DIR, ensure_directories
_LOGGING_CONFIGURED = False
def configure_logging() -> None:
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return
    ensure_directories()
    log_file: Path = LOG_DIR / "glaze.log"
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    _LOGGING_CONFIGURED = True
def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
