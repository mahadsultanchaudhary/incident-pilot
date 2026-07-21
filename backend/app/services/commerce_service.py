from sqlmodel import Session
from ..models import CartItem, Order, OrderItem, OrderStatus, Product, User
from ..schemas import CartAddRequest, CartLine, CartResponse
from ..repositories import StoreRepository


class CommerceService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = StoreRepository(session)

    def cart(self, user_id: int) -> CartResponse:
        lines: list[CartLine] = []
        for item in self.repo.cart_items(user_id):
            product = self.repo.product(item.product_id)
            if product:
                lines.append(CartLine(product_id=product.id, product_name=product.name, quantity=item.quantity,
                    unit_price_cents=product.price_cents, subtotal_cents=product.price_cents * item.quantity))
        return CartResponse(items=lines, total_cents=sum(line.subtotal_cents for line in lines))

    def add_to_cart(self, user_id: int, request: CartAddRequest) -> CartResponse:
        product = self.repo.product(request.product_id)
        if not product or product.inventory < request.quantity:
            raise ValueError("Product is unavailable in the requested quantity")
        item = next((row for row in self.repo.cart_items(user_id) if row.product_id == request.product_id), None)
        if item:
            item.quantity += request.quantity
        else:
            self.session.add(CartItem(user_id=user_id, product_id=request.product_id, quantity=request.quantity))
        self.session.commit()
        return self.cart(user_id)

    def checkout(self, user: User, payment_token: str) -> Order:
        cart = self.cart(user.id)
        if not cart.items:
            raise ValueError("Cart is empty")
        if payment_token.startswith("fail_"):
            raise RuntimeError("Payment gateway declined authorization")
        order = Order(user_id=user.id, total_cents=cart.total_cents, status=OrderStatus.paid,
                      payment_reference=f"pay_{payment_token[-8:]}")
        self.session.add(order)
        self.session.flush()
        for line in cart.items:
            product = self.repo.product(line.product_id)
            assert product
            product.inventory -= line.quantity
            self.session.add(OrderItem(order_id=order.id, product_id=line.product_id, product_name=line.product_name,
                quantity=line.quantity, unit_price_cents=line.unit_price_cents))
        for item in self.repo.cart_items(user.id):
            self.session.delete(item)
        self.session.commit()
        self.session.refresh(order)
        return order
