from pydantic import BaseModel


class PhotoDetails(BaseModel):
    fileName: str
    fileType: str
    base64: str
    quantity: int


class PhotosUploadPostBodyRequest(BaseModel):
    photos: list[PhotoDetails]
