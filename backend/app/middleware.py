import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .logging_config import logger, request_context

access_log = logger("incidentpilot.access")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        correlation_id = request.headers.get("X-Correlation-ID", request_id)
        user_id = request.headers.get("X-User-ID", "anonymous")
        context = {"request_id": request_id, "correlation_id": correlation_id, "user_id": user_id}
        token = request_context.set(context)
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            latency = round((time.perf_counter() - started) * 1000, 2)
            access_log.exception("Request failed", extra={"endpoint": request.url.path, "method": request.method,
                "status_code": 500, "latency_ms": latency})
            raise
        finally:
            request_context.reset(token)
        latency = round((time.perf_counter() - started) * 1000, 2)
        access_log.info("Request completed", extra={"endpoint": request.url.path, "method": request.method,
            "status_code": response.status_code, "latency_ms": latency})
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        return response
