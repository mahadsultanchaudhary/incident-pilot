import json
from datetime import datetime, timezone
from typing import Any


class LogParser:
    """Normalizes JSON application logs and conventional plain-text records."""
    def parse(self, raw: str) -> dict[str, Any]:
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            event = {"message": raw, "level": "INFO", "service": "unknown"}
        timestamp = event.get("timestamp") or datetime.now(timezone.utc).isoformat()
        return {"timestamp": timestamp, "level": str(event.get("level", "INFO")).upper(),
                "service": event.get("service", "store-api"), "message": event.get("message", ""),
                "request_id": event.get("request_id"), "correlation_id": event.get("correlation_id"),
                "trace": event.get("trace"), "context": event.get("context", {})}
