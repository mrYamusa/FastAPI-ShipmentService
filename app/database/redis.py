from redis.asyncio import Redis
from app.config import database_settings
import os

redis_url = Redis(os.getenv("REDIS_URL"))

if redis_url:
    _token_blacklist = Redis.from_url(os.getenv("REDIS_URL"))
else:
    _token_blacklist = Redis(
        host=database_settings.REDIS_HOST,
        port=database_settings.REDIS_PORT,
        db=0,
    )


async def add_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted")


async def check_if_blacklisted(jti: str):
    status = bool(await _token_blacklist.exists(jti))
    return status
