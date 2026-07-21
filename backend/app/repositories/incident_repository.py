from sqlmodel import Session, select
from ..models import Evidence, Incident, LogEvent


class IncidentRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_incidents(self) -> list[Incident]:
        return list(self.session.exec(select(Incident).order_by(Incident.last_seen.desc())))

    def get(self, incident_id: int) -> Incident | None:
        return self.session.get(Incident, incident_id)

    def events(self, incident: Incident) -> list[LogEvent]:
        return list(self.session.exec(
            select(LogEvent).where(LogEvent.service == incident.service).order_by(LogEvent.timestamp.desc()).limit(100)
        ))

    def evidence(self, incident_id: int) -> list[Evidence]:
        return list(self.session.exec(select(Evidence).where(Evidence.incident_id == incident_id)))
