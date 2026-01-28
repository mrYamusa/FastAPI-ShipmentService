from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.database.models import User
from fastapi import HTTPException, status
from sqlmodel import select
from passlib.context import CryptContext
from app.utils import encode_token

ctx = CryptContext(schemes={"sha256_crypt"}, deprecated="auto")

"""
For future reference the userdata is a pydantic model from 
the api.schemas module and has a password field. 
to use this pydantic model which is user data we first use
the .model_dump() method to convert this pydantic model 
to a dictionary. We then use the ** unpacking operator 
to pass the dictionary items as keyword arguments to the
User model constructor.

essentially converting this user_data pydantic model to 
the User model, we also need  to exclude using 
exclude={"password"} in .model_dump() and hash it before storing 
it in the database.
the User child models like Seller have a hashed_password field
not a password field but the hashed_password field has 
an `hashed_password = Field(exclude=True)`.

"""


class UserService(BaseService):
    def __init__(self, session: AsyncSession, model: User):
        super().__init__(model=model, session=session)

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password) -> str:
        user = await self._get_by_email(email)
        if user is None or not ctx.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email or password is incorrect",
            )

        return encode_token(
            data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),
                }
            },
        )

    async def _get(self, user_id):
        return await self._get(self.model, user_id)

    async def _add_user(self, user_data):
        data = self.model(
            **user_data.model_dump(exclude={"password"}),
            password_hash=ctx.hash(user_data.password),
        )
        return await self._create(entity=data)

    async def _update(self, user_data):
        return await self._create(user_data)

    async def _delete(self, user_id):
        user = await self._get(user_id)
        await self.session.delete(user)
        await self.session.commit()
