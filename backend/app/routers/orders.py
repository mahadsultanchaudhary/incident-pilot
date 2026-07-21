from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from ..dependencies import SessionDep, current_user
from ..models import Order, User
from ..schemas import CheckoutRequest, OrderRead
from ..services import CommerceService

router = APIRouter(prefix="/api", tags=["orders", "payments"])
UserDep = Annotated[User, Depends(current_user)]


@router.get("/orders", response_model=list[OrderRead])
def list_orders(session: SessionDep, user: UserDep):
    return list(session.exec(select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc())))


@router.post("/checkout", response_model=OrderRead)
def checkout(payload: CheckoutRequest, session: SessionDep, user: UserDep):
    try: return CommerceService(session).checkout(user, payload.payment_token)
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc: raise HTTPException(status_code=502, detail=str(exc)) from exc
