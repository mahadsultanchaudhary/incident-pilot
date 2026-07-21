from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from ..models import Incident, IncidentStatus, LogEvent
from ..repositories import IncidentRepository
from ..parser import StackTraceExtractor
from .incident_detector import IncidentDetector


class IncidentService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = IncidentRepository(session)
        self.trace_extractor = StackTraceExtractor()

    def record_event(self, event: LogEvent) -> LogEvent:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        if event.level in {"ERROR", "CRITICAL"}:
            self._detect(event)
        return event

    def _detect(self, event: LogEvent) -> None:
        IncidentDetector(self.session).detect(event)

    def detail(self, incident_id: int) -> dict:
        incident = self.repo.get(incident_id)
        if not incident:
            raise LookupError("Incident not found")
        events = self.repo.events(incident)
        return {"incident": incident, "events": events, "evidence": self.repo.evidence(incident_id),
                "stack_trace": self.trace_extractor.extract(next((e.trace for e in events if e.trace), None))}

    def dashboard(self) -> dict:
        incidents = self.repo.list_incidents()
        events = list(self.session.exec(select(LogEvent).order_by(LogEvent.timestamp.desc()).limit(40)))
        services = ["checkout-api", "payment-worker", "catalog-api", "auth-api", "redis-cache"]
        health = []
        for service in services:
            failures = sum(e.service == service and e.level == "ERROR" for e in events)
            health.append({"service": service, "status": "degraded" if failures else "healthy",
                           "availability": max(91.2, 99.98 - failures * 1.7), "latency": 48 + failures * 42})
        today = datetime.now(timezone.utc).date()
        frequency = [{"day": (today - timedelta(days=offset)).strftime("%a"), "incidents": sum(i.first_seen.date() == today - timedelta(days=offset) for i in incidents)} for offset in range(6, -1, -1)]
        return {"open_incidents": sum(i.status != IncidentStatus.resolved for i in incidents),
                "critical_incidents": sum(i.severity == "critical" for i in incidents),
                "events_processed": len(events), "mean_time_to_detect": "2m 14s", "service_health": health,
                "logs": events, "incidents": incidents[:8], "frequency": frequency,
                "error_distribution": [{"name": "Application", "value": 44}, {"name": "Database", "value": 26},
                    {"name": "Auth", "value": 18}, {"name": "Cache", "value": 12}]}
