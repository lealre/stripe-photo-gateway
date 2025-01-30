import base64
import os

import pytest
from botocore import client
from celery.exceptions import TaskError
from pytest_mock import MockerFixture

from src.core.settings import settings
from src.integrations.email.email_integration import email
from src.schemas.orders import OrderRequestPayload
from src.worker.tasks import (
    task_send_new_order_email_notification,
    task_store_photos_in_s3,
)


async def test_aws_s3_task_function_success(
    s3_client: client.BaseClient, payload_order: OrderRequestPayload
) -> None:
    bucket_name = settings.AWS_S3_BUCKET_NAME
    s3_client.create_bucket(Bucket=bucket_name)
    folder_name = 'test-folder'

    result = task_store_photos_in_s3(payload_order, folder_name)

    assert result == {'message': 'Photos stored in S3 successfully'}

    for n, photo in enumerate(payload_order.orderInfo.photos):
        file_name = photo.fileName
        file_type_extension = photo.fileType.split('/')[1]
        file_name = f'Photo-{n + 1:02}.{file_type_extension}'
        s3_path = os.path.join(folder_name, file_name)

        response = s3_client.get_object(Bucket=bucket_name, Key=s3_path)
        uploaded_content = response['Body'].read()

        base64_encoded_content = photo.base64.split(',')[1].encode('utf-8')
        decoded_content = base64.b64decode(base64_encoded_content)

        assert uploaded_content == decoded_content


async def test_aws_s3_task_function_fail(
    s3_client: client.BaseClient, payload_order: OrderRequestPayload
) -> None:
    bucket_name = 'other-bucket-name'
    s3_client.create_bucket(Bucket=bucket_name)
    folder_name = 'test-folder'

    with pytest.raises(TaskError, match='Failed to store'):
        task_store_photos_in_s3(payload_order, folder_name)


def test_email_task_function_success(payload_order: OrderRequestPayload) -> None:
    email.config.SUPPRESS_SEND = 1

    with email.record_messages() as outbox:
        result = task_send_new_order_email_notification(payload_order, 'folder-name')

        assert len(outbox) == 1
        assert outbox[0]['Subject'] == 'Nova Solicitação de ordem'
        assert outbox[0]['To'] == settings.HOST_EMAIL
        assert result == {'message': 'Notification email sent successfully.'}


def test_email_task_function_fail(
    payload_order: OrderRequestPayload, mocker: MockerFixture
) -> None:
    email.config.SUPPRESS_SEND = 1

    mock_send_email = mocker.patch(
        'src.worker.tasks.send_email', side_effect=Exception()
    )

    with pytest.raises(TaskError, match='Failed to send email:'):
        task_send_new_order_email_notification(payload_order, 'folder-name')

    mock_send_email.assert_called_once()
