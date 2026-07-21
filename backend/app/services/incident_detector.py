import hashlib
from datetime import datetime, timezone
from sqlmodel import Session, select
from ..models import Evidence, Incident, LogEvent
from ..parser import StackTraceExtractor


class IncidentDetector:
    def __init__(self, session: Session):
        self.session = session
        self.extractor = StackTraceExtractor()

    def detect(self, event: LogEvent) -> None:
        signature = self.extractor.extract(event.trace)
        fingerprint = hashlib.sha256(f"{event.service}:{signature['exception'] or event.message[:80]}".encode()).hexdigest()[:24]
        incident = self.session.exec(select(Incident).where(Incident.fingerprint == fingerprint)).first()
        now = datetime.now(timezone.utc)
        if incident:
            incident.last_seen, incident.occurrence_count = now, incident.occurrence_count + 1
            incident.root_cause_confidence = min(0.97, 0.5 + incident.occurrence_count * 0.08)
        else:
            incident = Incident(title=f"{event.service}: {signature['exception'] or event.message[:56]}", severity="critical" if "Error" in str(signature["exception"]) else "high", service=event.service, summary=str(signature["message"] or event.message), first_seen=now, last_seen=now, root_cause_confidence=0.58, fingerprint=fingerprint)
            self.session.add(incident); self.session.flush()
        self.session.add(Evidence(incident_id=incident.id, event_id=event.id, assertion=f"{event.level} from {event.service}: {event.message}", relevance=0.94))
        self.session.commit()
