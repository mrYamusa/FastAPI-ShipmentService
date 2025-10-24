from pydantic import BaseModel, Field, EmailStr


class BaseSeller(BaseModel):
    name: str
    email: EmailStr


class CreateSeller(BaseSeller):
    password: str


class SellerRead(BaseSeller):
    pass
