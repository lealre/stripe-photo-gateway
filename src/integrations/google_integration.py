from http import HTTPStatus

import httpx
from pydantic import ValidationError

from src.core.settings import settings
from src.schemas.integrations import (
    AddressValidationSchema,
    GoogleAddressValidationAPIResponse,
)


async def verify_address(adress_string: str) -> AddressValidationSchema:
    """
    Verifies the validity of an address using the Google Geocoding API.

    :param address_string: A string representing the full address to be validated.
    :return: An instance of `AddressValidationSchema` containing the validation status,
            a message, and the formatted address if valid.
    """
    params = {'address': adress_string, 'key': settings.GOOGLE_API_KEY}

    validation_response = AddressValidationSchema(
        is_validated=False, message='', formatted_address=None
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(settings.GOOGLE_VALIDATION_API_URL, params=params)

        if response.status_code != HTTPStatus.OK:
            validation_response.message = 'API response error'
            return validation_response

    try:
        response_data = GoogleAddressValidationAPIResponse(**response.json())
    except ValidationError:
        validation_response.message = 'Validation fields error'
        return validation_response

    if not response_data.results:
        validation_response.message = 'Address not found'
        return validation_response

    if len(response_data.results) > 1:
        validation_response.message = 'Address is ambiguous'
        return validation_response

    addrress = response_data.results[0]

    for info in addrress.address_components:
        if 'country' in info['types']:
            if 'PT' not in info['short_name']:
                validation_response.message = 'Address is not in Portugal'
                return validation_response

    return AddressValidationSchema(
        is_validated=True,
        message='Address validated',
        formatted_address=addrress.formatted_address,
    )
