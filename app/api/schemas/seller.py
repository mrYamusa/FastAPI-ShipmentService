from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class Role(str, Enum):
    seller = "Seller"
    costumer = "Costumer"
    super_admin = "SuperAdmin"
    admin1 = "Admin1"
    admin2 = "Admin2"
    admin3 = "Admin3"


class BaseSeller(BaseModel):
    name: str
    email: EmailStr
    address: int


class CreateSeller(BaseSeller):
    password: str
    role: Role = Field(default=Role.seller)


from app.database.models import Shipments


class SellerRead(BaseSeller):
    role: Role = Field(default=Role.seller)
    shipment: list[Shipments] = Field(default=[], description="List of shipment IDs")
