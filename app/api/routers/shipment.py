from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.database.session import SessionDep
from app.database.models import ShipmentStatus
from sqlmodel import select
from app.api.schemas.shipment import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)  # , ShipmentStatus
from app.api.dependencies import SellerDep2
from rich import print, panel

# from pydantic import BaseModel
from app.database.models import Shipments

# from app.services.shipment import ShipmentService
from app.api.dependencies import ServiceDep, SellerDep2

router = APIRouter(prefix="/shipment", tags=["Shipments"])


@router.post("/create", response_model=ShipmentRead)  # , response_model=ShipmentCreate)
async def submit_shipment(body: ShipmentCreate, service: ServiceDep, token: SellerDep2):
    if body.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight is above shipment limits! \nMaximum weight limit is 25",
        )
    return await service.add(body, seller=token)


# @router.get("/latest")
# async def get_latest_shipment(session: SessionDep, token: str = Depends(oauth2_scheme)):
#     data = decode_token(token=token)
#     if data in ["Token has expired", "Invalid token"]:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=data,
#         )
#     else:
#         from sqlalchemy import func

#         statement = select(func.max(Shipments.id))
#         result = await session.execute(statement)
#         id = result.scalar()  # gets the single value from the result
#         shipment = await session.get(Shipments, id)
#         return shipment


@router.get("/latest")
async def get_latest_shipment(session: SessionDep, user: SellerDep2):
    from rich import print, panel

    a = f"{user}"
    print(panel.Panel(a, style="green"))

    from sqlalchemy import func

    statement = select(func.max(Shipments.id))
    result = await session.execute(statement)
    id = result.scalar()  # gets the single value from the result
    shipment = await session.get(Shipments, id)
    return shipment


@router.get("/item", response_model=ShipmentRead)
async def get_shipment(id: UUID, service: ServiceDep):
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The ID {id} you provided doesn't exist",
        )
    return shipment


@router.put("/update")
async def shipment_update(id: UUID, shipment: ShipmentUpdate, service: ServiceDep):
    return await service.update(id, shipment)


# @router.patch("/shipment", response_model=ShipmentRead)
# async def shipment_patch(id: int, body: ShipmentUpdate):  # dict[str, ShipmentStatus]):
#     shipment = db.update_shipment(id=id, shipment=body)
#     db.close()
#     return shipment


@router.delete("/delete")
async def delete_shipment(id: UUID, service: ServiceDep):
    return await service.delete(id=id)
    # return {"Detail": f"Shipment with #{id} has been deleted Successfully"}
