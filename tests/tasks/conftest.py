import base64
import os
from dataclasses import dataclass

import pytest

from src.schemas.orders import (
    CustomerInfo,
    OrderRequestPayload,
    PhotoDetails,
    PhotosUploadPayload,
)


@dataclass
class EncodedPhotoDataClass:
    fileName: str
    fileType: str
    encodedData: str


@pytest.fixture
def encoded_photos() -> list[EncodedPhotoDataClass]:
    photos_test_directory = 'tests/utils/photos'

    photos_path = [
        os.path.join(photos_test_directory, file)
        for file in os.listdir(photos_test_directory)
        if os.path.isfile(os.path.join(photos_test_directory, file))
    ]

    encoded_files = []

    for file_path in photos_path:
        with open(file_path, 'rb') as file:
            file_content = file.read()

            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.png':
                mime_type = 'image/png'
            elif file_extension in {'.jpg', '.jpeg'}:
                mime_type = 'image/jpeg'
            else:
                mime_type = 'application/octet-stream'

            encoded_content = base64.b64encode(file_content).decode('utf-8')

            encoded_photo = EncodedPhotoDataClass(
                fileName=os.path.basename(file_path),
                fileType=mime_type,
                encodedData=f'data:{mime_type};base64,{encoded_content}',
            )

            encoded_files.append(encoded_photo)

    return encoded_files


@pytest.fixture
def payload_order(encoded_photos: list[EncodedPhotoDataClass]) -> OrderRequestPayload:
    photos_details_schema: list[PhotoDetails] = []

    for photo in encoded_photos:
        photos_details_schema.append(
            PhotoDetails(
                fileName=photo.fileName,
                base64=photo.encodedData,
                quantity=1,
                fileType=photo.fileType,
            )
        )

    order_info_schema = PhotosUploadPayload(photos=photos_details_schema)

    customer_info = CustomerInfo(
        customerEmail='test@email.com',
        phoneNumber='1234567890',
        formattedAddress='123 Main St, Example City, 98765',
    )

    payload = OrderRequestPayload(
        orderId=1,
        customerInfo=customer_info,
        orderInfo=order_info_schema,
    )

    return payload
