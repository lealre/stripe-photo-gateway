from pydantic import BaseModel, EmailStr


class PhotoDetails(BaseModel):
    fileName: str
    fileType: str
    base64: str
    quantity: int


class PhotosUploadPayload(BaseModel):
    photos: list[PhotoDetails]


class CustomerInfo(BaseModel):
    customerEmail: EmailStr
    phoneNumber: str
    formattedAddress: str


class CreateCheckoutSessionPayload(CustomerInfo):
    address: str
    city: str
    postalCode: str


class OrderRequestPayload(BaseModel):
    orderId: int
    customerInfo: CustomerInfo
    orderInfo: PhotosUploadPayload
