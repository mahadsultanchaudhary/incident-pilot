from fastapi import APIRouter, HTTPException
from ..ai import AIAnalysisService
from ..dependencies import SessionDep
from ..schemas import AnalysisRequest, AnalysisResponse, ChatRequest, IncidentRead, PostmortemRequest
from ..services import IncidentService

router = APIRouter(prefix="/api", tags=["incidents"])


@router.get("/incidents", response_model=list[IncidentRead])
def list_incidents(session: SessionDep): return IncidentService(session).repo.list_incidents()


@router.get("/incidents/{incident_id}")
def incident_detail(incident_id: int, session: SessionDep):
    try:
        detail = IncidentService(session).detail(incident_id)
        return {"incident": detail["incident"], "events": detail["events"], "evidence": detail["evidence"], "stack_trace": detail["stack_trace"]}
    except LookupError as exc: raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/analyze", response_model=AnalysisResponse)
def analyze(payload: AnalysisRequest, session: SessionDep):
    service = IncidentService(session)
    try: detail = service.detail(payload.incident_id)
    except LookupError as exc: raise HTTPException(status_code=404, detail=str(exc)) from exc
    analysis = AIAnalysisService().analyze(detail["incident"], detail["events"])
    detail["incident"].ai_analysis = analysis
    session.add(detail["incident"]); session.commit()
    return {"incident_id": payload.incident_id, **analysis}


@router.post("/chat")
def chat(payload: ChatRequest, session: SessionDep):
    service = IncidentService(session)
    try: detail = service.detail(payload.incident_id)
    except LookupError as exc: raise HTTPException(status_code=404, detail=str(exc)) from exc
    analysis = detail["incident"].ai_analysis or AIAnalysisService().analyze(detail["incident"], detail["events"])
    return {"answer": AIAnalysisService().answer(detail["incident"], payload.question, analysis)}


@router.post("/postmortem")
def postmortem(payload: PostmortemRequest, session: SessionDep):
    service = IncidentService(session)
    try: detail = service.detail(payload.incident_id)
    except LookupError as exc: raise HTTPException(status_code=404, detail=str(exc)) from exc
    analysis = detail["incident"].ai_analysis or AIAnalysisService().analyze(detail["incident"], detail["events"])
    return {"markdown": AIAnalysisService().postmortem(detail["incident"], analysis)}


@router.get("/dashboard")
def dashboard(session: SessionDep): return IncidentService(session).dashboard()
