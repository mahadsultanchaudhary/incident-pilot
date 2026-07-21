import os
import time
from fastapi import APIRouter, HTTPException, Request
from ..services.security import verify_token

router = APIRouter(prefix="/api/system", tags=["production-bug-lab"])


@router.post("/bugs/missing-field")
async def missing_field(request: Request):
    payload = await request.json()
    return {"customer": payload["customer_id"]}


@router.get("/bugs/divide-by-zero")
def divide_by_zero(): return {"result": 100 / 0}


@router.get("/bugs/database-timeout")
def database_timeout():
    raise TimeoutError("sqlite3.OperationalError: database is locked after 5000ms")


@router.get("/bugs/invalid-jwt")
def invalid_jwt(): return verify_token("definitely.not-a-valid-token")


@router.get("/bugs/redis-unavailable")
def redis_unavailable(): raise ConnectionError("redis.exceptions.ConnectionError: Error 111 connecting to redis:6379")


@router.get("/bugs/missing-env")
def missing_env(): return {"secret": os.environ["PAYMENT_PROVIDER_PRIVATE_KEY"]}


@router.get("/bugs/permission-error")
def permission_error():
    with open("/root/incidentpilot-restricted.log", "w") as stream: stream.write("forbidden")
    return {"ok": True}


@router.post("/bugs/malformed-payload")
async def malformed_payload(request: Request):
    payload = await request.json()
    return {"total": payload["items"] + 1}
