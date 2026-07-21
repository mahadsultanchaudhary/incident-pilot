from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from ..dependencies import SessionDep, admin_user
from ..models import Product, User
from ..schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(session: SessionDep):
    return list(session.exec(select(Product).order_by(Product.name)))


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product: raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductRead, status_code=201)
def create_product(payload: ProductCreate, session: SessionDep, _: Annotated[User, Depends(admin_user)]):
    product = Product(**payload.model_dump())
    session.add(product); session.commit(); session.refresh(product)
    return product
