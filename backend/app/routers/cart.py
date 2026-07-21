from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import SessionDep, current_user
from ..models import User
from ..schemas import CartAddRequest, CartResponse
from ..services import CommerceService

router = APIRouter(prefix="/api/cart", tags=["cart"])
UserDep = Annotated[User, Depends(current_user)]


@router.get("", response_model=CartResponse)
def get_cart(session: SessionDep, user: UserDep): return CommerceService(session).cart(user.id)


@router.post("/items", response_model=CartResponse)
def add_item(payload: CartAddRequest, session: SessionDep, user: UserDep):
    try: return CommerceService(session).add_to_cart(user.id, payload)
    except ValueError as exc: raise HTTPException(status_code=409, detail=str(exc)) from exc
