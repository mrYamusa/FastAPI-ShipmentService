from app.services.base import BaseService
from app.database.models import Shipments, ShipmentStatus, ShipmentEvent
from app.services.notifications import NotificationsService


class ShipmentEventService(BaseService):
    def __init__(self, session, tasks):
        super().__init__(model=ShipmentEvent, session=session)
        self.notification_service = NotificationsService(tasks)

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
        await self._notify(shipment=shipment, status=status)

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

    async def _notify(self, shipment: Shipments, status: ShipmentStatus):
        if status == ShipmentStatus.in_transit:
            return

        subject: str
        context: dict
        template_name: str

        match status:
            case ShipmentStatus.delivered:
                recipients = [shipment.client_contact_email]
                subject = "Shipment Delivered 📦"
                context = {
                    "content": shipment.content,
                    "id": shipment.id,
                    "seller_name": "FastShip Client",
                    "destination": shipment.destination,
                    "estimated_delivery": shipment.estimated_delivery,
                }
                template_name = "mail_delivered.html"

            case ShipmentStatus.out_for_delivery:
                recipients = [shipment.client_contact_email]
                subject = "Shipment Out for Delivery ⛟"
                context = {
                    "content": shipment.content,
                    "id": shipment.id,
                    "seller_name": "FastShip Client",
                    "destination": shipment.destination,
                    "estimated_delivery": shipment.estimated_delivery,
                }
                template_name = "mail_out_for_delivery.html"

            case ShipmentStatus.placed:
                recipients = [shipment.client_contact_email]
                subject = "Shipment Placed ⌯⌲"
                context = {
                    "content": shipment.content,
                    "id": shipment.id,
                    "seller_name": "FastShip Client",
                    "destination": shipment.destination,
                    "delivery_partner": shipment.delivery_partner.name.upper(),
                }
                template_name = "mail_placed.html"

            case ShipmentStatus.cancelled:
                recipients = [shipment.client_contact_email]
                subject = "Shipment Cancelled ❌"
                context = {
                    "content": shipment.content,
                    "id": shipment.id,
                    "seller_name": "FastShip Client",
                    "destination": shipment.destination,
                }
                template_name = "mail_cancelled.html"

        await self.notification_service.send_email_with_template(
            recipients=recipients,
            subject=subject,
            context=context,
            template_name=template_name,
        )
