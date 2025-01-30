import io
import os

from botocore import client

from src.integrations.aws_integration import store_in_s3


async def test_aws_s3_integration(s3_client: client.BaseClient):
    bucket_name = 'test-bucket-name'
    s3_client.create_bucket(Bucket=bucket_name)

    file_content = b'Test file content'
    file_like = io.BytesIO(file_content)
    file_name = 'test_file.txt'
    folder_name = 'test_folder'

    store_in_s3(file_like, file_name, folder_name, bucket_name)

    s3_path = os.path.join(folder_name, file_name)
    response = s3_client.get_object(Bucket=bucket_name, Key=s3_path)
    uploaded_content = response['Body'].read()

    assert uploaded_content == file_content
