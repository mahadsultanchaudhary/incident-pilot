import asyncio
import logging
import random
import traceback
from datetime import datetime, timezone
from sqlmodel import Session
from ..database import engine
from ..models import LogEvent
from .incident_service import IncidentService

traffic_log = logging.getLogger("incidentpilot.traffic")


async def generate_production_traffic(interval: float) -> None:
    services = ["catalog-api", "checkout-api", "payment-worker", "auth-api", "redis-cache"]
    messages = ["GET /products completed", "Order status updated", "Cart inventory validated", "Payment authorization succeeded"]
    failures = [("checkout-api", "Payment provider timeout after 3000ms", "TimeoutError: upstream payment gateway timed out"),
                ("redis-cache", "Redis connection refused", "ConnectionError: redis cache unavailable"),
                ("payment-worker", "Database transaction retry exhausted", "OperationalError: database is locked")]
    while True:
        await asyncio.sleep(interval)
        is_failure = random.random() < 0.18
        service, message, trace = random.choice(failures) if is_failure else (random.choice(services), random.choice(messages), None)
        level = "ERROR" if is_failure else ("WARNING" if random.random() < 0.12 else "INFO")
        event = LogEvent(timestamp=datetime.now(timezone.utc), level=level, service=service, message=message,
            endpoint="/api/checkout" if service == "checkout-api" else "/api/products", status_code=500 if is_failure else 200,
            latency_ms=random.randint(30, 3200), correlation_id=f"traffic-{random.randint(100, 999)}", trace=trace)
        with Session(engine) as session:
            IncidentService(session).record_event(event)
        traffic_log.log(getattr(logging, level), message, extra={"service": service, "event_type": "synthetic_traffic"})
