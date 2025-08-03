import abc


class Logger(abc.ABC):
    """Logger."""

    @abc.abstractmethod
    def info(self, message: str) -> None:
        """Log an info message."""

    @abc.abstractmethod
    def error(self, message: str) -> None:
        """Log an error message."""
