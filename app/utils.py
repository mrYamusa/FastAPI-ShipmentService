from fastapi import HTTPException, status
from app.core.security import oauth2_scheme_seller
from typing import Annotated
from fastapi import Depends
import jwt
from uuid import uuid4
from app.config import token_settings
from datetime import timedelta, datetime, timezone


def encode_token(data: dict, expiry=timedelta(minutes=token_settings.EXP_TIME)) -> str:
    token = jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        key=token_settings.SECRET_KEY,
        algorithm=token_settings.HASH_ALGO,
    )
    return token


from pathlib import Path

APP_DIR = Path(__file__).parent
TEMPLATES_DIR = APP_DIR / "templates"


async def decode_token(token: Annotated[str, Depends(oauth2_scheme_seller)]):
    try:
        data = jwt.decode(
            jwt=token,
            key=token_settings.SECRET_KEY,
            algorithms=token_settings.HASH_ALGO,
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # print("Done decoding")
    return data


# print(
#     decode_token(
#         "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InNlbGxlcl9uYW1lIjoibnlhLm11c2EiLCJzZWxsZXJfZW1haWwiOiJpY3NpZGF2aWRAZ21haWwuY29tIn0sImV4cCI6MTc2MTMxOTQzNH0.lyjf0GxwBE_l43qSt-iyw9Xn0OnKFoagLof6TkPA2hs"
#     )
# )
# gege = {
#     "user": {
#         "seller_name": "nya.musa",
#         "seller_email": "icsidavid@gmail.com",
#     },
#     "exp": 1761319434,
# }
# print(gege["user"]["seller_name"])
