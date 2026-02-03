from app.api.schemas.shipment import (
    # ShipmentCreate,
    # ShipmentRead,
    # ShipmentStatus,
    ShipmentUpdate,
)
from app.database.models import (
    Shipments,
    ShipmentStatus,
    Sellers,
    DeliveryPartners,
)
from app.api.schemas.shipment import ShipmentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.services.base import BaseService
from uuid import UUID
from rich import panel, print
from app.services.delivery_partner import DeliveryPartnerService

# from app.api.dependencies import PartnerDep2
from app.services.shipment_event import ShipmentEventService


class ShipmentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService,
    ):
        super().__init__(model=Shipments, session=session)
        self.partner_service = partner_service
        self.event_service = event_service

    async def get(self, id: UUID) -> Shipments:
        shipment = await self._get(id)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The shipment with id {id} you provided doesn't exist",
            )
        return shipment

    async def update(self, id, body: ShipmentUpdate, partner: DeliveryPartners):
        # shipment.sqlmodel_update(body)

        shipment = await self.get(id)
        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBDDEN,
                detail="You are not authorized to update this Shipment",
            )
        if body.content or body.weight or body.estimated_delivery:
            shipment.content = body.content if body.content else shipment.content
            shipment.weight = body.weight if body.weight else shipment.weight
            shipment.estimated_delivery = (
                body.estimated_delivery
                if body.estimated_delivery
                else shipment.estimated_delivery
            )
        update_for_event = body.model_dump(
            exclude={"content", "weight", "estimated_delivery"},
            exclude_none=True,
        )
        if "status" in update_for_event or "location" in update_for_event:
            await self.event_service.add(**update_for_event, shipment=shipment)

        return await self._update(shipment)

    async def add(self, shipment: ShipmentCreate, seller: Sellers):
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found, cannot create shipment",
            )
        shipment_instance = Shipments(
            **shipment.model_dump(exclude_none=False),
            status=ShipmentStatus.placed,
            seller_id=seller.id,
        )
        partner = await self.partner_service.assign_shipment_to_delivery_partner(
            shipment=shipment_instance
        )
        shipment_instance.delivery_partner_id = partner.id
        await self.event_service.add(
            shipment=shipment_instance,
            location=seller.zip_code,
            status=ShipmentStatus.placed,
            description=f"Shipment placed at seller location {seller.zip_code}\nAssigned to delivery partner {partner.name}",
        )

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

    async def cancel(self, id: UUID, seller: Sellers) -> Shipments:
        shipment = await self.get(id)
        if seller.id != shipment.seller_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not Authorized to Cancel Shipment",
            )
        event = await self.event_service.add(
            shipment=shipment, status=ShipmentStatus.cancelled
        )
        # shipment.timeline.append(event)
        return shipment
