from pydantic import BaseModel, Field
from random import randint
from enum import Enum
from datetime import datetime, timedelta
from app.api.schemas.seller import BaseSeller


def random_destination():
    return randint(11000, 11999)


def delivery_date(est_time: int = 3):
    return datetime.utcnow() + timedelta(est_time)


class ShipmentStatus(str, Enum):
    placed = "Placed!"
    in_transit = "In Transit"
    out_for_delivery = "Out for Delivery"
    delivered = "Delivered"


class BaseShipments(BaseModel):
    content: str | None = Field(description="Product Name", max_length=30)
    weight: float = Field(description="Weight of product in Kilograms", le=25, gt=0)
    destination: int | None = Field(
        description="Delivery location", default_factory=random_destination
    )


class ShipmentRead(BaseShipments):
    status: ShipmentStatus = Field(
        default=ShipmentStatus.placed, description="Shipment Status", max_length=20
    )
    seller: BaseSeller = Field(description="Seller details")


class Order(BaseModel):
    price: int
    title: str
    description: str


class ShipmentCreate(BaseShipments):
    order: Order | None = Field(default=None, description="Order details")
    estimated_delivery: datetime | None = Field(
        default_factory=delivery_date, description="Estimated delivery date"
    )
    destination: int | None = Field(
        default_factory=random_destination, description="Delivery location"
    )


class ShipmentUpdate(BaseModel):
    content: str | None = Field(
        max_length=20, default=None
    )  # default None -> makes the field not required
    status: ShipmentStatus = Field(
        default=ShipmentStatus.placed, description="Shipment Status", max_length=20
    )
    weight: float | None = Field(
        le=25,
        gt=0,
        description="Weight of Package in Kgs",
        default=None,
    )
