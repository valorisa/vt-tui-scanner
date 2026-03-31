"""
Logging configuration for VT Scanner.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

_loggers = {}


def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = "vt_scanner.log",
    max_bytes: int = 10485760,
    backup_count: int = 5
) -> logging.Logger:
    """Setup application logger."""
    logger = logging.getLogger("vt_scanner")
    logger.setLevel(getattr(logging, level.upper()))
    
    logger.handlers = []
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
    
    
def get_logger(name: str = "vt_scanner") -> logging.Logger:
    """Get logger instance."""
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
    return _loggers[name]
