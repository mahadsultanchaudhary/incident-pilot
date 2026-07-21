from ..models import LogEvent


class TimelineBuilder:
    def build(self, events: list[LogEvent]) -> list[dict[str, str]]:
        return [{"timestamp": item.timestamp.isoformat(), "event": item.message, "level": item.level}
                for item in sorted(events, key=lambda event: event.timestamp)[:12]]
