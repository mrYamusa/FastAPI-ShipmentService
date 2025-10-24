from fastapi import APIRouter, Depends
from app.api.schemas.seller import CreateSeller, SellerRead
from app.api.dependencies import SellerDep
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter(prefix="/seller", tags=["Sellers"])


@router.post("/create")
async def create_seller(seller: CreateSeller, service: SellerDep):
    new_seller = await service.create_seller(seller)
    return SellerRead(**new_seller.model_dump())


@router.post("/token")
async def login_seller(
    service: SellerDep, request_form: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await service.token(request_form.username, request_form.password)
