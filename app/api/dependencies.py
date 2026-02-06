from sqlalchemy.ext.asyncio import AsyncSession
from app.services.shipment_event import ShipmentEventService
from fastapi import Depends, HTTPException, status, BackgroundTasks
from app.database.session import create_session
from app.database.redis import check_if_blacklisted
from typing import Annotated
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.services.delivery_partner import DeliveryPartnerService
from app.core.security import oauth2_scheme_seller, oauth2_scheme_partner
from app.utils import decode_token
from app.database.models import Sellers, DeliveryPartners
from uuid import UUID


"""
get an async session as a dependency using create session in database sessions file
"""
SessionDep = Annotated[AsyncSession, Depends(create_session)]

"""
Use the session gotten above to create a `chained dependency` 

Shipment service contains functons that need an async session to modify and get 
items in database. here we pass in that session as a dependency
"""


def get_shipment_service(session: SessionDep, tasks: BackgroundTasks):
    return ShipmentService(
        session=session,
        partner_service=DeliveryPartnerService(session=session),
        event_service=ShipmentEventService(session=session, tasks=tasks),
    )


def get_seller_service(session: SessionDep):
    return SellerService(session=session)


def get_partner_service(session: SessionDep):
    return DeliveryPartnerService(session=session)


def get_shipment_event_service(session: SessionDep):
    return ShipmentEventService(session=session)


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
PartnerDep = Annotated[DeliveryPartnerService, Depends(get_partner_service)]


async def get_access_token(token: str) -> dict:
    data = await decode_token(token)
    # print(data)
    if data is None or await check_if_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token maybe invalid or expired",
        )
    return data


async def get_seller_token(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
) -> dict:
    return await get_access_token(token)


async def get_partner_token(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
) -> dict:
    return await get_access_token(token)


async def get_seller(
    token_data: Annotated[dict, Depends(get_seller_token)], session: SessionDep
):
    if token_data in ["Token has expired", "Invalid token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or Invalid Token",
        )
    print(str(token_data["user"]["id"]))
    user = await session.get(Sellers, UUID(token_data["user"]["id"]))
    return user


async def get_partner(
    token_data: Annotated[dict, Depends(get_partner_token)], session: SessionDep
):
    if token_data in ["Token has expired", "Invalid token"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or Invalid Token",
        )

    partner = await session.get(
        entity=DeliveryPartners, ident=UUID(token_data["user"]["id"])
    )
    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Authorized.",
        )
    return partner


"""
SellerDep2 is what is being used to authenticate
it returns a seller if they exist by verifying the provided token 
it depends on the `get_user` function which provides authenticated user data
`get_user` depends on the `decode_token` function which verifies the token's validity
"""
SellerDep2 = Annotated[Sellers, Depends(get_seller)]
PartnerDep2 = Annotated[DeliveryPartners, Depends(get_partner)]
