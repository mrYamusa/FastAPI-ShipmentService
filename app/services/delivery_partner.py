from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.api.schemas.delivery_partner import CreatePartner, UpdatePartner
from app.database.models import DeliveryPartners
from sqlmodel import select, any_
from passlib.context import CryptContext
from uuid import UUID
from .user import UserService
from typing import Sequence
from app.database.models import Shipments

password_context = CryptContext(schemes=["sha256_crypt"])


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=DeliveryPartners)

    async def create_partner(self, partner: CreatePartner):
        return await self._add_user(partner)

    async def update_partner(self, update_data):
        return await self._update(user_data=update_data)

    async def get_partner_by_zipcode(self, zip_code: int) -> Sequence[DeliveryPartners]:
        partners = (
            await self.session.scalars(
                select(DeliveryPartners).where(
                    zip_code == any_(DeliveryPartners.serviceable_codes)
                )
            )
        ).all()
        print("----------Partners---------\n", partners)
        return partners

    async def assign_shipment_to_delivery_partner(self, shipment: Shipments):
        elligible_partners = await self.get_partner_by_zipcode(shipment.destination)
        # shipment.delivery_partner_id = partners[0].id if partners else None
        for partner in elligible_partners:
            print("----------Partner Name---------\n", partner.name)
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="No delivery partner available for this shipment at the moment",
        )

    async def get_partner(self, id: UUID) -> DeliveryPartners | None:
        partner = await self.session.get(entity=DeliveryPartners, ident=id)
        await self.session.commit()
        return partner

    async def delete_partner(self):
        pass

    async def token(self, email, password) -> dict:
        token = await self._generate_token(email, password)
        return {"access_token": token, "type": "JWT"}

        # self.session.get(DeliveryPartners, id)
