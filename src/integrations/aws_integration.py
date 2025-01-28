import io
import os

import boto3

from src.core.settings import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION,
)


def store_in_s3(
    file_like: io.BytesIO, file_name: str, folder_name: str, bucket_name: str
) -> None:
    s3_path = os.path.join(folder_name, file_name)

    s3_client.upload_fileobj(file_like, bucket_name, s3_path)
