from sqlmodel import SQLModel, Field, Relationship, Column
from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from datetime import datetime


class User(SQLModel):
    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)


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
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            primary_key=True,
            default=uuid4,
        )
    )
    content: str
    weight: float = Field(le=25)
    status: ShipmentStatus = Field(default=ShipmentStatus.placed)
    estimated_delivery: datetime
    destination: int
    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            postgresql.TIMESTAMP,
            default=datetime.utcnow,
        )
    )

    seller_id: UUID = Field(foreign_key="Sellers.id")  # __tablename__ of Sellers table
    seller: "Sellers" = Relationship(
        back_populates="shipment", sa_relationship_kwargs={"lazy": "selectin"}
    )
    delivery_partner_id: UUID = Field(foreign_key="DeliveryPartners.id")
    delivery_partner: "DeliveryPartners" = Relationship(
        back_populates="shipment", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Sellers(User, table=True):
    __tablename__ = (
        "Sellers"  # used in foreign key reference for seller_id in Shipments
    )
    # id: int = Field(default=None, primary_key=True)
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    name: str
    email: EmailStr
    address: int = Field(description="Zip code of the seller's location")
    password_hash: str
    role: Role = Field(default=Role.seller)

    shipment: list[Shipments] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            postgresql.TIMESTAMP,
            default=datetime.utcnow,
        )
    )


# from sqlalchemy.dialects import postgresql


class DeliveryPartners(User, table=True):
    __tablename__ = "DeliveryPartners"
    id: UUID = Field(
        sa_column=Column(
            "id",
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    serviceable_codes: list[int] = Field(
        sa_column=Column(postgresql.ARRAY(postgresql.INTEGER))
    )
    created_at: datetime = Field(
        sa_column=Column(
            "created_at",
            postgresql.TIMESTAMP,
            default=datetime.utcnow,
        )
    )
    maximum_capacity: int
    shipment: list[Shipments] = Relationship(
        back_populates="delivery_partner",
        cascade_delete=True,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
