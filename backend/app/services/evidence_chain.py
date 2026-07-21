from ..models import Evidence, LogEvent


class EvidenceChainBuilder:
    def build(self, evidence: list[Evidence], events: list[LogEvent]) -> list[dict[str, object]]:
        event_by_id = {event.id: event for event in events}
        chain = [{"assertion": item.assertion, "relevance": item.relevance,
                  "timestamp": (event_by_id.get(item.event_id).timestamp if event_by_id.get(item.event_id) else item.created_at).isoformat()}
                 for item in evidence]
        return sorted(chain, key=lambda item: float(item["relevance"]), reverse=True)
