import json
from http import HTTPStatus

from httpx import AsyncClient
from redis.asyncio import Redis as asyncRedis

from src.core.settings import settings
from src.schemas.orders import PhotoDetails, PhotosUploadPayload


async def test_upload_photos_ok(
    async_client: AsyncClient,
    photos_upload_order: PhotosUploadPayload,
    redis_client: asyncRedis,
) -> None:
    response = await async_client.post(
        '/orders/upload/photos', json=photos_upload_order.model_dump()
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Successfully stored in Redis'}
    assert 'session_id' in response.cookies
    assert response.cookies['session_id']

    session_id_value = response.cookies['session_id']

    cached_info = await redis_client.get(session_id_value)
    expiration_info = await redis_client.ttl(session_id_value)

    assert cached_info is not None
    assert expiration_info == settings.REDIS_EXPIRATION_TIME

    photos_info = PhotosUploadPayload(
        photos=[PhotoDetails(**photo) for photo in json.loads(cached_info)]
    )

    total_photos_in_cache = len(photos_info.photos)

    assert total_photos_in_cache == len(photos_upload_order.photos)

    for n in range(total_photos_in_cache):
        assert photos_info.photos[n].base64 == photos_upload_order.photos[n].base64
        assert photos_info.photos[n].fileName == photos_upload_order.photos[n].fileName
        assert photos_info.photos[n].fileType == photos_upload_order.photos[n].fileType
