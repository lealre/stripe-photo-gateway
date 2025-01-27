import json
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from integrations import google_integration
from src.api.dependencies import RedisClient
from src.core.settings import settings
from src.schemas.integrations import AddressValidationSchema, ValidateAddressInfoRequest
from src.schemas.orders import PhotosUploadPostBodyRequest

router = APIRouter()


@router.post('/upload/photos')
async def upload_photos(
    payload: PhotosUploadPostBodyRequest, redis_client: RedisClient
):
    """
    Stores photos in redis
    """
    photos_json = json.dumps([photo.model_dump_json() for photo in payload.photos])

    await redis_client.set('photos', photos_json)

    return {'message': 'Successfully stored in Redis'}


@router.post('/address/validate')
async def validate_customer_address(
    payload: ValidateAddressInfoRequest, cache: RedisClient
) -> AddressValidationSchema:
    """
    Validates the customer address.

    If it results in just one location and if its in Portugal.
    """
    address_info = payload.model_dump()

    address_string = ' '.join([
        str(value) for key, value in address_info.items() if key != 'phoneNumber'
    ]).strip()

    if await cache.exists(address_string):
        cached_address = await cache.get(address_string)
        address_validation = AddressValidationSchema(**json.loads(cached_address))
    else:
        address_validation = await google_integration.verify_address(address_string)
        cache_value = address_validation.model_dump_json()
        await cache.set(address_string, cache_value, ex=settings.REDIS_EXPIRATION_TIME)

    if not address_validation.is_validated:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=address_validation.message
        )

    return address_validation
