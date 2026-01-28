from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from app.database.models import Shipments
from enum import Enum


class ServicableZipCodes(int, Enum):
    pass


class BasePartner(BaseModel):
    name: str = Field(max_length=25)
    email: EmailStr


class CreatePartner(BasePartner):
    serviceable_codes: list[int]
    maximum_capacity: int
    password: str


class ReadPartner(BasePartner):
    serviceable_codes: list[int]
    created_at: datetime
    maximum_capacity: int
    shipments: list[Shipments]


class UpdatePartner(BaseModel):
    serviceable_codes: list[int] | None = Field(default=None)
    maximum_capacity: int | None = Field(default=None)
