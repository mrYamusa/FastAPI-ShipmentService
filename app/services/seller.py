from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Sellers
from app.api.schemas.seller import CreateSeller
from passlib.context import CryptContext
from sqlalchemy import select
from fastapi import HTTPException, status
from app.utils import encode_token

password_context = CryptContext(schemes=["sha256_crypt"])


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_seller(self, seller: CreateSeller) -> Sellers:
        new_seller = Sellers(
            **seller.model_dump(exclude={"password"}),
            password_hash=password_context.hash(seller.password),
        )

        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)
        return new_seller

    async def token(self, email, password):
        result = await self.session.execute(
            select(Sellers).where(Sellers.email == email)
        )
        seller = result.scalar()
        if seller is None or not password_context.verify(
            password, seller.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The Email or Password was not found",
            )
        token = encode_token(
            data={
                "user": {
                    "seller_name": seller.name,
                    "seller_id": seller.id,
                },
            },
        )
        return {"access_token": token, "type": "JWT"}
