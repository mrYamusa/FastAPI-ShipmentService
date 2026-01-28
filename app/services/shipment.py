from app.api.schemas.shipment import (
    # ShipmentCreate,
    # ShipmentRead,
    # ShipmentStatus,
    ShipmentUpdate,
)
from app.database.models import Shipments, ShipmentStatus, Sellers
from app.api.schemas.shipment import ShipmentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.services.base import BaseService
from uuid import UUID
from rich import panel, print
from app.services.delivery_partner import DeliveryPartnerService


class ShipmentService(BaseService):
    def __init__(self, session: AsyncSession, partner_service: DeliveryPartnerService):
        super().__init__(model=Shipments, session=session)
        self.partner_service = partner_service

    async def get(self, id: UUID) -> Shipments | None:
        return await self._get(id)

    async def update(self, id, body: ShipmentUpdate):
        fetched_shipment = await self.session.get(Shipments, id)
        if fetched_shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The ID {id} you provided doesn't exist",
            )

        fetched_shipment.sqlmodel_update(body)
        return await self._update(fetched_shipment)

    async def add(self, shipment: ShipmentCreate, seller: Sellers):
        shipment_instance = Shipments(
            **shipment.model_dump(exclude_none=False),
            status=ShipmentStatus.placed,
            seller_id=seller.id,
        )
        partner = await self.partner_service.assign_shipment_to_delivery_partner(
            shipment=shipment_instance
        )
        shipment_instance.delivery_partner_id = partner.id

        print(panel.Panel(f"{seller.id}", style="blue"))
        return await self._create(shipment_instance)

    async def delete(self, id: UUID):
        shipment_item = await self.get(id)
        if not shipment_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
            )
        await self._delete(shipment_item)
        return {"Detail": f"Shipment with #{id} has been deleted Successfully"}
