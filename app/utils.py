from app.core.security import oauth2_scheme
from typing import Annotated
from fastapi import Depends
import jwt
from app.config import token_settings


def encode_token():
    pass


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
    jwt.decode(
        jwt=token,
        key=token_settings.SECRET_KEY,
        algorithms=token_settings.HASH_ALGO,
    )
    pass
