from app.api.schemas.shipment import (
    # ShipmentCreate,
    # ShipmentRead,
    # ShipmentStatus,
    ShipmentUpdate,
)
from app.database.models import Shipments, ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int, database_table):
        return await self.session.get(database_table, id)

    async def update(self, id, body: ShipmentUpdate):
        thing = await self.session.get(Shipments, id)
        if thing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The ID {id} you provided doesn't exist",
            )
        # for key, value in shipment.model_dump(exclude_unset=True).items():
        #     setattr(thing, key, value)
        thing.status = ShipmentStatus(body.status.value)
        self.session.add(thing)
        await self.session.commit()
        await self.session.refresh(thing)
        return thing

    async def post(self, shipment: Shipments):
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

    async def delete(self, id):
        item = self.get(id)
        await self.session.delete(item)
        await self.session.commit()
        return {"Detail": f"Shipment with #{id} has been deleted Successfully"}
