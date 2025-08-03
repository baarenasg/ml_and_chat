import logging
import traceback
from .settings import LoggerConfig


class Logger():
    """Class to manage the logger of the application."""

    def __init__(self, logger_config: "LoggerConfig"):
        formatter = logging.Formatter(
            fmt=logger_config.LOGGER_FORMAT,
            datefmt=logger_config.LOGGER_DATE_FORMAT
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(int(logger_config.LOG_LEVEL))

        log = logging.getLogger(logger_config.LOG_NAME)
        log.handlers = [handler]

        self.log = log
        self.log.info("Logger initialize with level %s",
                      logger_config.LOG_LEVEL)

    def info(self, msg: str, **kwargs):
        """Log a message with severity 'INFO' on this logger."""
        self.log.info(msg, **kwargs)

    def error(self, msg: str, **kwargs):
        """Log a message with severity 'ERROR' on this logger."""
        self.log.error(msg, **kwargs)

    def debug(self, msg: str, **kwargs):
        """Log a message with severity 'DEBUG' on this logger."""
        self.log.debug(msg, **kwargs)

    def exceptions_handler(self, msg, **kwargs):
        """Specifies the error trace and log the error."""
        trace = traceback.format_exc(limit=1).replace("\n", "")
        self.error(f"{msg} - {trace.strip()}", **kwargs)
