import base64
import hashlib
import hmac
import json
import time
from fastapi import HTTPException, status
from ..config import get_settings


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(user_id: int, is_admin: bool) -> str:
    payload = {"sub": str(user_id), "admin": is_admin, "exp": int(time.time()) + 3600 * 12}
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    signature = hmac.new(get_settings().jwt_secret.encode(), encoded.encode(), hashlib.sha256).hexdigest()
    return f"{encoded}.{signature}"


def verify_token(token: str) -> dict:
    try:
        encoded, signature = token.rsplit(".", 1)
        expected = hmac.new(get_settings().jwt_secret.encode(), encoded.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise ValueError("signature mismatch")
        payload = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        if payload["exp"] < time.time():
            raise ValueError("token expired")
        return payload
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token") from exc
