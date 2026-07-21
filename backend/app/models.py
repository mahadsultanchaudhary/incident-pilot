from datetime import datetime, timezone
from enum import Enum
from typing import Any
from sqlmodel import SQLModel, Field, Column, JSON


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    failed = "failed"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    display_name: str
    password_hash: str
    is_admin: bool = False
    created_at: datetime = Field(default_factory=utcnow)


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sku: str = Field(index=True, unique=True)
    name: str
    description: str
    price_cents: int
    inventory: int = 0
    service: str = "catalog-api"
    created_at: datetime = Field(default_factory=utcnow)


class CartItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = 1


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    status: OrderStatus = OrderStatus.pending
    total_cents: int
    payment_reference: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    product_name: str
    quantity: int
    unit_price_cents: int


class LogEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=utcnow, index=True)
    level: str = Field(index=True)
    service: str = Field(index=True)
    message: str
    endpoint: str | None = None
    request_id: str | None = Field(default=None, index=True)
    correlation_id: str | None = Field(default=None, index=True)
    user_id: str | None = None
    status_code: int | None = None
    latency_ms: float | None = None
    trace: str | None = None
    context: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class IncidentStatus(str, Enum):
    investigating = "investigating"
    resolved = "resolved"
    monitoring = "monitoring"


class Incident(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    severity: str = Field(index=True)
    status: IncidentStatus = IncidentStatus.investigating
    service: str = Field(index=True)
    summary: str
    first_seen: datetime = Field(default_factory=utcnow)
    last_seen: datetime = Field(default_factory=utcnow)
    occurrence_count: int = 1
    root_cause_confidence: float = 0.0
    fingerprint: str = Field(index=True, unique=True)
    ai_analysis: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))


class Evidence(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    incident_id: int = Field(index=True, foreign_key="incident.id")
    event_id: int = Field(foreign_key="logevent.id")
    assertion: str
    relevance: float
    created_at: datetime = Field(default_factory=utcnow)
