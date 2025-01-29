import asyncio
import base64
import io
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from celery import group
from celery.exceptions import TaskError
from starlette.datastructures import UploadFile

from src.core.settings import settings
from src.integrations import aws_integration
from src.integrations.email.email_integration import send_email
from src.schemas.orders import OrderRequestPayload, PhotoDetails
from src.worker.worker_app import celery_app


@dataclass
class DecodedPhoto:
    file_like: io.BytesIO
    file_name: str


@celery_app.task(pydantic=True)
def task_store_photos_in_s3(
    payload: OrderRequestPayload, folder_name: str
) -> dict[str, str]:
    photos = payload.orderInfo.photos

    for n, photo in enumerate(photos):
        photo_decoded = decode_photo(photo, n)

        try:
            aws_integration.store_in_s3(
                file_like=photo_decoded.file_like,
                file_name=photo_decoded.file_name,
                folder_name=folder_name,
                bucket_name=settings.AWS_S3_BUCKET_NAME,
            )
        except Exception as e:
            raise TaskError(
                f'Failed to store {photo_decoded.file_name} in S3: {str(e)}'
            )

    return {'message': 'Photos stored in S3 successfully'}


@celery_app.task(pydantic=True)
def task_send_new_order_email_notification(
    payload: OrderRequestPayload, folder_name: str
) -> dict[str, str]:
    photos = payload.orderInfo.photos

    email_attachments: list[UploadFile | str | dict[Any, Any]] = []
    email_template_body: dict[str, Any] = {
        'photos': [],
        'addressInfo': payload.customerInfo.model_dump(),
        'folderName': folder_name,
    }

    for n, photo in enumerate(photos):
        photo_decoded = decode_photo(photo, n)

        template_info = photo.model_dump()
        template_info['fileName'] = photo_decoded.file_name
        email_template_body['photos'].append(template_info)

        upload_file = UploadFile(
            file=photo_decoded.file_like,
            filename=photo_decoded.file_name,
        )
        email_attachments.append(upload_file)

    try:
        asyncio.run(
            send_email(
                subject='Nova Solicitação de ordem',
                recipients=[settings.HOST_EMAIL],
                attachments=email_attachments,
                template_body=email_template_body,
                template_name='new_order_notification.html',
            )
        )
    except Exception as e:
        raise TaskError(f'Failed to send email: {str(e)}')

    return {'message': 'Notification email sent successfully.'}


@celery_app.task(pydantic=True)
def task_notify_and_store_photos(payload: OrderRequestPayload) -> None:
    """
    Orchestrates the photo processing workflow.
    """
    order_id = payload.orderId
    folder_name = f'orders/{datetime.now().strftime("%Y/%m/%d")}/order-{order_id}'
    payload_dict = payload.model_dump()

    workflow = group(
        task_store_photos_in_s3.s(payload_dict, folder_name),
        task_send_new_order_email_notification.s(payload_dict, folder_name),
    )

    workflow()


def decode_photo(photo: PhotoDetails, n: int) -> DecodedPhoto:
    base64_str = photo.base64.split(',')[1]

    file_type_extension = photo.fileType.split('/')[1]
    photo_number = n + 1
    file_name = f'Photo-{photo_number:02}.{file_type_extension}'

    file_data = base64.b64decode(base64_str)
    file_like = io.BytesIO(file_data)

    return DecodedPhoto(file_like=file_like, file_name=file_name)
