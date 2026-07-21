from ..models import LogEvent


class RequestCorrelator:
    def group(self, events: list[LogEvent]) -> dict[str, list[LogEvent]]:
        groups: dict[str, list[LogEvent]] = {}
        for event in events:
            key = event.correlation_id or event.request_id or f"event-{event.id}"
            groups.setdefault(key, []).append(event)
        return groups
