import asyncio
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import notification_settings

fastmail = FastMail(
    config=ConnectionConfig(
        **notification_settings.model_dump(),
    )
)


async def send_message():
    await fastmail.send_message(
        message=MessageSchema(
            recipients=["icsidavid@gmail.com"],
            subject="Your Package Has Been Delivered By Fastship",
            body="✨Things are about to get interesting...",
            subtype=MessageType.plain,
        )
    )
    return {"message": "email has been sent"}


asyncio.run(send_message())
