from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.session import create_session
from typing import Annotated
from app.services.seller import SellerService
from app.services.shipment import ShipmentService

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
ServiceDep can be called in an endpoint and used to make database interactions
e.g 
@app.get(/shipment)
async def get_shipment(id: int, service: ServiceDep)
    service.get(id)
"""
ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerDep = Annotated[SellerService, Depends(get_seller_service)]
