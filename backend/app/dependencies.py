from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session
from .database import get_session
from .models import User
from .services.security import verify_token

bearer = HTTPBearer(auto_error=False)
SessionDep = Annotated[Session, Depends(get_session)]


def current_user(session: SessionDep, credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    claims = verify_token(credentials.credentials)
    user = session.get(User, int(claims["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def admin_user(user: Annotated[User, Depends(current_user)]) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")
    return user
