import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from .config import get_settings
from .database import create_db_and_tables, engine
from .logging_config import configure_logging, logger
from .middleware import RequestContextMiddleware
from .models import Product, User
from .models import LogEvent
from .services.incident_service import IncidentService
from .routers import all_routers
from .services.security import hash_password
from .services.traffic import generate_production_traffic

app_log = logger("incidentpilot")


def seed_data() -> None:
    with Session(engine) as session:
        if not session.exec(select(User).where(User.email == "admin@incidentpilot.local")).first():
            session.add(User(email="admin@incidentpilot.local", display_name="Incident Admin", password_hash=hash_password("incidentpilot"), is_admin=True))
        if not session.exec(select(Product)).first():
            session.add_all([Product(sku="OBS-001", name="Observability Plan", description="Managed telemetry subscription", price_cents=12900, inventory=250),
                Product(sku="INC-002", name="Incident Response Kit", description="On-call readiness toolkit", price_cents=4900, inventory=80),
                Product(sku="SRE-003", name="SRE Workshop", description="Team incident simulation", price_cents=19900, inventory=25)])
        session.commit()
        if not session.exec(select(LogEvent)).first():
            IncidentService(session).record_event(LogEvent(level="ERROR", service="checkout-api", endpoint="/api/checkout",
                message="Payment provider timeout after 3000ms", status_code=504, latency_ms=3004, request_id="req-7d31a",
                correlation_id="corr-checkout-401", trace="Traceback (most recent call last):\n  File \"services/payments.py\", line 84, in authorize\n    gateway.charge(token)\nTimeoutError: upstream payment gateway timed out after 3000ms"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    create_db_and_tables()
    seed_data()
    task = asyncio.create_task(generate_production_traffic(get_settings().traffic_interval_seconds))
    yield
    task.cancel()


app = FastAPI(title="IncidentPilot", version="1.0.0", lifespan=lifespan)
app.add_middleware(RequestContextMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
for router in all_routers: app.include_router(router)


@app.get("/health")
def health(): return {"status": "ok", "service": "incidentpilot-api"}


@app.exception_handler(Exception)
async def unexpected_error(_: Request, exc: Exception):
    app_log.exception("Unhandled application error")
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error_type": type(exc).__name__})
