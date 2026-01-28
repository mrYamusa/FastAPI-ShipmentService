from fastapi import APIRouter, Depends, HTTPException, status
from app.api.schemas.delivery_partner import CreatePartner, ReadPartner, UpdatePartner
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import get_partner_token, PartnerDep, PartnerDep2
from typing import Annotated
from app.database.redis import add_to_blacklist

router = APIRouter(prefix="/delivery_partner", tags=["Delivery Partner"])
"""
create service for adding, reading, updating, deleting partner
"""


@router.post("/create")
async def create_partner(
    partner: CreatePartner,
    service: PartnerDep,
):
    return await service.create_partner(partner)


@router.post("/token")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], service: PartnerDep
) -> dict:
    token = await service.token(form.username, form.password)
    return token


@router.put("/update", response_model=ReadPartner)
async def update_partner(
    update_data: UpdatePartner, partner: PartnerDep2, session: PartnerDep
):
    update = update_data.model_dump(exclude_none=True)

    if not update:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )
    partner = await session.update_partner(partner.sqlmodel_update(update))
    return partner


@router.post("/logout")
async def logout_partner(token: Annotated[str, Depends(get_partner_token)]):
    await add_to_blacklist(token)
    return {"status": "Black listed successfully"}
