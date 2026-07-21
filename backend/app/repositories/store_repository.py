from sqlmodel import Session, select
from ..models import CartItem, Product, User


class StoreRepository:
    def __init__(self, session: Session):
        self.session = session

    def products(self) -> list[Product]:
        return list(self.session.exec(select(Product).order_by(Product.name)))

    def product(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def user_by_email(self, email: str) -> User | None:
        return self.session.exec(select(User).where(User.email == email)).first()

    def cart_items(self, user_id: int) -> list[CartItem]:
        return list(self.session.exec(select(CartItem).where(CartItem.user_id == user_id)))
