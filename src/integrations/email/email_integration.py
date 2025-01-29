from typing import Any

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.datastructures import UploadFile

from src.core.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_STARTTLS=settings.EMAIL_STARTTLS,
    MAIL_SSL_TLS=settings.EMAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=settings.TEMPLATE_FOLDER,
)

email = FastMail(config=conf)


async def send_email(  # noqa: PLR0917, PLR0913
    subject: str,
    recipients: list[str],
    template_name: str | None = None,
    body: str | None = None,
    attachments: list[UploadFile | str | dict[Any, Any]] = [],
    template_body: list[dict[str, Any]] | dict[str, Any] | None = None,
) -> None:
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
        attachments=attachments,
        template_body=template_body,
    )

    await email.send_message(message, template_name=template_name)
