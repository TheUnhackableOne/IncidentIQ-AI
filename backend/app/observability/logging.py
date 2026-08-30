"""Observability and logging setup."""

import json
import logging
import sys
from typing import Any


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


def setup_logging(log_level: str = "INFO") -> None:
    """Setup application logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    formatter = JSONFormatter()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set third-party loggers to WARNING
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


class LoggerMixin:
    """Mixin to provide logger to classes."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return logging.getLogger(self.__class__.__module__)


def log_with_context(extra: dict[str, Any] | None = None):
    """Decorator to add context to logs.
    
    Args:
        extra: Extra context to add to logs
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            context = extra or {}
            
            logger.info(
                f"Starting {func.__name__}",
                extra={"extra": {**context, "function": func.__name__}}
            )
            
            try:
                result = func(*args, **kwargs)
                logger.info(
                    f"Completed {func.__name__}",
                    extra={"extra": {**context, "function": func.__name__}}
                )
                return result
            except Exception as e:
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    extra={"extra": {**context, "function": func.__name__}},
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator
