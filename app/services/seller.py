from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Sellers
from app.api.schemas.seller import CreateSeller
from passlib.context import CryptContext
from sqlalchemy import select
from fastapi import HTTPException, status
from app.utils import encode_token
from .user import UserService

password_context = CryptContext(schemes=["sha256_crypt"])


class SellerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Sellers)

    async def create_seller(self, seller: CreateSeller) -> Sellers:
        return await self._add_user(seller)

    async def token(self, email, password):
        token: str = await self._generate_token(email=email, password=password)
        return {"access_token": token, "type": "JWT"}
