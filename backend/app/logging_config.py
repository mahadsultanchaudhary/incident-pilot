import json
import logging
import traceback
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import get_settings

request_context: ContextVar[dict[str, str]] = ContextVar("request_context", default={})


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {"timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"), "level": record.levelname,
                   "logger": record.name, "message": record.getMessage(), **request_context.get()}
        for name in ("endpoint", "method", "status_code", "latency_ms", "service", "event_type"):
            if hasattr(record, name):
                payload[name] = getattr(record, name)
        if record.exc_info:
            payload["trace"] = "".join(traceback.format_exception(*record.exc_info))
        return json.dumps(payload, default=str)


def configure_logging() -> None:
    settings = get_settings()
    path = Path(settings.log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(path, maxBytes=5_000_000, backupCount=3)
    handler.setFormatter(JsonFormatter())
    console = logging.StreamHandler()
    console.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    root.addHandler(console)


def logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
