from app.services.base import BaseService
from app.database.models import Shipments, ShipmentStatus, ShipmentEvent


class ShipmentEventService(BaseService):
    def __init__(self, session):
        super().__init__(model=ShipmentEvent, session=session)

    async def add(
        self,
        shipment: Shipments,
        location: int = None,
        status: ShipmentStatus = None,
        description: str = None,
    ) -> ShipmentEvent:
        if not location or not status:
            latest = await self.get_latest_event(shipment)
            location = location if location else latest.location
            status = status if status else latest.status

        shipment_event = ShipmentEvent(
            location=location,
            status=status,
            description=description
            if description
            else self.generate_description(location, status),
            shipment=shipment,
        )
        return await self._create(shipment_event)

    async def get_latest_event(self, shipment: Shipments):
        timeline = shipment.timeline
        if not timeline:
            return None
        timeline.sort(key=lambda item: item.created_at)
        return timeline[-1]

    def generate_description(self, location, status):
        match status:
            case ShipmentStatus.placed:
                return f"Shipment placed at location {location}\nAssigned to delivery partner"
            case ShipmentStatus.out_for_delivery:
                return "Shipment is out for delivery at location."
            case ShipmentStatus.delivered:
                return f"Shipment has been delivered at location {location}"
            case ShipmentStatus.cancelled:
                return (
                    f"Shipment was cancelled by the Seller at location * {location} *"
                )
            case _:
                return f"Shipment is {status} and scanned at location * {location} *"
