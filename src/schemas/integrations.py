from typing import Any

from pydantic import BaseModel


class GoogleAddressResultSchema(BaseModel):
    address_components: list
    formatted_address: str
    geometry: dict[str, Any]
    place_id: str
    types: list


class GoogleAddressValidationAPIResponse(BaseModel):
    results: list[GoogleAddressResultSchema]
    status: str


class ValidateAddressInfoRequest(BaseModel):
    address: str
    city: str
    phoneNumber: int
    postalCode: int


class AddressValidationSchema(BaseModel):
    is_validated: bool
    message: str
    formatted_address: str | None
