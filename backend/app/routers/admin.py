from fastapi import APIRouter, Depends
from sqlmodel import select
from ..dependencies import SessionDep, admin_user
from ..models import Order, User

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/orders")
def all_orders(session: SessionDep, _: User = Depends(admin_user)):
    return list(session.exec(select(Order).order_by(Order.created_at.desc())))
