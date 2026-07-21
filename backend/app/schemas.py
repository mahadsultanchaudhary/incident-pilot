from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from .models import IncidentStatus, OrderStatus


class ProductCreate(BaseModel):
    sku: str
    name: str
    description: str
    price_cents: int = Field(gt=0)
    inventory: int = Field(ge=0)


class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    service: str


class RegisterRequest(BaseModel):
    email: str
    display_name: str
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CartAddRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, le=20)


class CartLine(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price_cents: int
    subtotal_cents: int


class CartResponse(BaseModel):
    items: list[CartLine]
    total_cents: int


class CheckoutRequest(BaseModel):
    payment_token: str = Field(min_length=4)


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: OrderStatus
    total_cents: int
    payment_reference: str | None
    created_at: datetime


class IncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    severity: str
    status: IncidentStatus
    service: str
    summary: str
    first_seen: datetime
    last_seen: datetime
    occurrence_count: int
    root_cause_confidence: float


class AnalysisRequest(BaseModel):
    incident_id: int


class ChatRequest(BaseModel):
    incident_id: int
    question: str = Field(min_length=2, max_length=1000)


class PostmortemRequest(BaseModel):
    incident_id: int


class AnalysisResponse(BaseModel):
    incident_id: int
    executive_summary: str
    timeline: list[dict[str, Any]]
    root_cause: str
    confidence: float
    affected_services: list[str]
    suggested_fixes: list[str]
    next_steps: list[str]
    evidence: list[dict[str, Any]]
