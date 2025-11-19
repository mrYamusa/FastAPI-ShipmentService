from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.database.session import create_session
from app.database.redis import check_if_blacklisted
from typing import Annotated
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.core.security import oauth2_scheme
from app.utils import decode_token
from app.database.models import Sellers


"""
get an async session as a dependency using create session in database sessions file
"""
SessionDep = Annotated[AsyncSession, Depends(create_session)]

"""
Use the session gotten above to create a `chained dependency` 

Shipment service contains functons that need an async session to modify and get 
items in database. here we pass in that session as a dependency
"""


def get_shipment_service(session: SessionDep):
    return ShipmentService(session=session)


def get_seller_service(session: SessionDep):
    return SellerService(session=session)


"""
ServiceDep can be called in an endpoint and used 
to make database interactions with shipment database
e.g 
@app.get(/shipment)
async def get_shipment(id: int, service: ServiceDep)
    service.get(id)
"""
ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerDep = Annotated[SellerService, Depends(get_seller_service)]


async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    data = await decode_token(token)
    print(data)
    if data is None or await check_if_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token maybe invalid or expired",
        )
    return data


from uuid import UUID


async def get_user(
    token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep
):
    if token_data in ["Token has expired", "Invalid token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or Invalid Token",
        )
    print(str(token_data["user"]["seller_id"]))
    user = await session.get(Sellers, UUID(token_data["user"]["seller_id"]))
    return user


# async def get_user(
#     token_data: Annotated[dict, Depends(decode_token)], session: SessionDep
# ):
#     if token_data in ["Token has expired", "Invalid token"]:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token expired or Invalid Token",
#         )
#     print(token_data["user"]["seller_id"])
#     user = await session.get(Sellers, token_data["user"]["seller_id"])
#     return user


"""
SellerDep2 is what is being used to authenticate
it returns a seller if they exist by verifying the provided token 
it depends on the `get_user` function which provides authenticated user data
`get_user` depends on the `decode_token` function which verifies the token's validity
"""
SellerDep2 = Annotated[Sellers, Depends(get_user)]

# def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
#     data = jwt.decode(
#         jwt=token, key=token_settings.SECRET_KEY, algorithms=token_settings.HASH_ALGO
#     )
#     if data in ["Token has expired", "Invalid token"]:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=data,
#         )
#     # return data["user"]["seller_name"], data["user"]["seller_email"]
#     return data["user"]["seller_email"]


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InNlbGxlcl9uYW1lIjoiWWFtdXNhIiwic2VsbGVyX2VtYWlsIjoiaWNzaWRhdmlkQGdtYWlsLmNvbSJ9LCJleHAiOjE3NjE3MTcwODB9.a66BCNfthq0V19aHAcXN5e-_USkbnne8r7JddppgA28

# get_user_data = Annotated[dict, Depends(get_user)]
