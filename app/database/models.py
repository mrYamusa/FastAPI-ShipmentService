from sqlmodel import SQLModel, Field, Relationship, Column
from datetime import datetime
from enum import Enum
from pydantic import EmailStr


class ShipmentStatus(str, Enum):
    placed = "Placed!"
    in_transit = "In Transit"
    out_for_delivery = "Out for Delivery"
    delivered = "Delivered"


class Role(str, Enum):
    seller = "Seller"
    costumer = "Costumer"
    super_admin = "SuperAdmin"
    admin1 = "Admin1"
    admin2 = "Admin2"
    admin3 = "Admin3"

from uuid import uuid4, UUID
class Shipments(SQLModel, table=True):
    __tablename__ = "Shipments"
    # id: int = Field(primary_key=True)
    id: UUID = Field(sa_column=Column())
    content: str
    weight: float = Field(le=25)
    status: ShipmentStatus = Field(default=ShipmentStatus.placed)
    estimated_delivery: datetime
    destination: int

    seller_id: int = Field(foreign_key="sellers.id")
    seller: "Sellers" = Relationship(back_populates="shipment", sa_relationship_kwargs={"lazy": "selectin"})


class Sellers(SQLModel, table=True):
    __tablename__ = "Sellers"
    id: int = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str
    role: Role = Field(default=Role.seller)

    shipment: list[Shipments] = Relationship(back_populates="seller", sa_relationship_kwargs={"lazy": "selectiin"})