from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import notification_settings
from fastapi import BackgroundTasks
from app.utils import TEMPLATES_DIR


class NotificationsService:
    def __init__(self, tasks: BackgroundTasks):
        self.fastmail = FastMail(
            config=ConnectionConfig(
                **notification_settings.model_dump(),
                TEMPLATE_FOLDER=TEMPLATES_DIR,
            )
        )
        self.tasks = tasks

    async def send_mail(
        self, recipients: list[str], subject: str, body: str, template_name: str
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                body=body,
                subtype=MessageType.html,
            ),
        )
        return {"message": "Notification sent successfully!"}

    async def send_email_with_template(
        self, recipients: list[str], subject: str, context: dict, template_name: str
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html,
            ),
            template_name=template_name,
        )

    async def send_notification(self, shipment, status):
        # Simulate sending a notification (e.g., email, SMS)
        print(f"Notification: Shipment {shipment.id} has been {status}.")
