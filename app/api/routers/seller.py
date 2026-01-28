from fastapi import APIRouter, Depends
from app.api.schemas.seller import CreateSeller, SellerRead
from app.api.dependencies import SellerDep, get_seller_token, SellerDep2

# from app.core.security import oauth2_scheme_seller
# from app.utils import decode_token
from app.api.dependencies import get_seller
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.database.redis import add_to_blacklist


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


@router.post("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_seller_token)]):
    await add_to_blacklist(token_data["jti"])
    return {"message": "Logout successful"}


# @router.post("/yoo")
# async def joyride(token: Annotated[str, Depends(oauth2_scheme)]):
#     data = decode_token(token=token)
#     return {"message": "Token decoded successfully", "data": data}
@router.post("/yoo")
async def joyride(token: SellerDep2):
    # data = decode_token(token=token)
    return {"message": "Token decoded successfully"}


@router.get("/myinfo", response_model=SellerRead)
async def my_info(user: Annotated[SellerRead, Depends(get_seller)]):
    return user
