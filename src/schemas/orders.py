from pydantic import BaseModel, EmailStr


class PhotoDetails(BaseModel):
    fileName: str
    fileType: str
    base64: str
    quantity: int


class PhotosUploadPayload(BaseModel):
    photos: list[PhotoDetails]


class CreateCheckoutSessionPayload(BaseModel):
    customerEmail: EmailStr
    phoneNumber: str
    address: str
    city: str
    postalCode: str
    formattedAddress: str
