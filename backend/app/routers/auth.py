from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from ..dependencies import SessionDep
from ..models import User
from ..schemas import LoginRequest, RegisterRequest, TokenResponse
from ..services.security import create_token, hash_password

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, session: SessionDep):
    if session.exec(select(User).where(User.email == payload.email)).first():
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=payload.email, display_name=payload.display_name, password_hash=hash_password(payload.password))
    session.add(user); session.commit(); session.refresh(user)
    return TokenResponse(access_token=create_token(user.id, user.is_admin))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, session: SessionDep):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or user.password_hash != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_token(user.id, user.is_admin))
