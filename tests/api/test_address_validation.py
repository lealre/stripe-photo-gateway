import json
from http import HTTPStatus
from unittest.mock import AsyncMock

from httpx import AsyncClient, Response
from pytest_mock import MockerFixture
from redis.asyncio import Redis as asyncRedis

from src.core.settings import settings
from tests.utils.mocked_google_responses import (
    google_mocked_respone_not_in_portugal,
    google_mocked_response_invalid_fields,
    google_mocked_response_multiple_results,
    google_mocked_response_results_empty,
    google_mocked_response_success,
)


async def test_address_verification_success(
    mocker: MockerFixture, async_client: AsyncClient
) -> None:
    mock_response = Response(
        status_code=HTTPStatus.OK,
        content=json.dumps(google_mocked_response_success),
        headers={'Content-Type': 'application/json'},
    )
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch('httpx.AsyncClient.get', new=mock_get)

    payload = {
        'address': 'Avenida Eusebio da Silva Ferreira',
        'city': 'Lisboa',
        'postalCode': 1500313,
        'phoneNumber': 123,
    }

    response = await async_client.post('/orders/address/validate', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'is_validated': True,
        'message': 'Address validated',
        'formatted_address': 'Av. Eusébio da Silva Ferreira, 1500-313 Lisboa, Portugal',
    }

    address_string = ' '.join([
        str(value) for key, value in payload.items() if key != 'phoneNumber'
    ]).strip()

    mock_get.assert_called_once_with(
        settings.GOOGLE_VALIDATION_API_URL,
        params={
            'address': address_string,
            'key': settings.GOOGLE_API_KEY,
        },
    )


async def test_address_verification_google_api_with_response_not_200(
    mocker: MockerFixture, async_client: AsyncClient
) -> None:
    mock_response = Response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=json.dumps(google_mocked_response_success),
        headers={'Content-Type': 'application/json'},
    )
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch('httpx.AsyncClient.get', new=mock_get)

    payload = {
        'address': 'Avenida Eusebio da Silva Ferreira',
        'city': 'Lisboa',
        'postalCode': 1500313,
        'phoneNumber': 123,
    }

    response = await async_client.post('/orders/address/validate', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'API response error'}

    address_string = ' '.join([
        str(value) for key, value in payload.items() if key != 'phoneNumber'
    ]).strip()

    mock_get.assert_called_once_with(
        settings.GOOGLE_VALIDATION_API_URL,
        params={
            'address': address_string,
            'key': settings.GOOGLE_API_KEY,
        },
    )


async def test_address_verification_results_field_empty_in_response(
    mocker: MockerFixture, async_client: AsyncClient
) -> None:
    mock_response = Response(
        status_code=HTTPStatus.OK,
        content=json.dumps(google_mocked_response_results_empty),
        headers={'Content-Type': 'application/json'},
    )
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch('httpx.AsyncClient.get', new=mock_get)

    payload = {
        'address': '123',
        'city': '123',
        'postalCode': 123,
        'phoneNumber': 123,
    }

    response = await async_client.post('/orders/address/validate', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Address not found'}

    address_string = ' '.join([
        str(value) for key, value in payload.items() if key != 'phoneNumber'
    ]).strip()

    mock_get.assert_called_once_with(
        settings.GOOGLE_VALIDATION_API_URL,
        params={
            'address': address_string,
            'key': settings.GOOGLE_API_KEY,
        },
    )


async def test_address_verification_response_with_validation_errors(
    mocker: MockerFixture, async_client: AsyncClient
) -> None:
    mock_response = Response(
        status_code=HTTPStatus.OK,
        content=json.dumps(google_mocked_response_invalid_fields),
        headers={'Content-Type': 'application/json'},
    )
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch('httpx.AsyncClient.get', new=mock_get)

    payload = {
        'address': '123',
        'city': '123',
        'postalCode': 123,
        'phoneNumber': 123,
    }

    response = await async_client.post('/orders/address/validate', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Validation fields error'}

    address_string = ' '.join([
        str(value) for key, value in payload.items() if key != 'phoneNumber'
    ]).strip()

    mock_get.assert_called_once_with(
        settings.GOOGLE_VALIDATION_API_URL,
        params={
            'address': address_string,
            'key': settings.GOOGLE_API_KEY,
        },
    )


async def test_address_verification_response_with_multiple_results(
    mocker: MockerFixture, async_client: AsyncClient
) -> None:
    mock_response = Response(
        status_code=HTTPStatus.OK,
        content=json.dumps(google_mocked_response_multiple_results),
        headers={'Content-Type': 'application/json'},
    )
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch('httpx.AsyncClient.get', new=mock_get)

    payload = {
        'address': '123',
        'city': '123',
        'postalCode': 123,
        'phoneNumber': 123,
    }

    response = await async_client.post('/orders/address/validate', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Address is ambiguous'}

    address_string = ' '.join([
        str(value) for key, value in payload.items() if key != 'phoneNumber'
    ]).strip()

    mock_get.assert_called_once_with(
        settings.GOOGLE_VALIDATION_API_URL,
        params={
            'address': address_string,
            'key': settings.GOOGLE_API_KEY,
        },
    )


async def test_address_verification_cache_in_redis(
    mocker: MockerFixture, async_client: AsyncClient, redis_client: asyncRedis
) -> None:
    mock_response = Response(
        status_code=HTTPStatus.OK,
        content=json.dumps(google_mocked_respone_not_in_portugal),
        headers={'Content-Type': 'application/json'},
    )
    mock_get = AsyncMock(return_value=mock_response)
    mocker.patch('httpx.AsyncClient.get', new=mock_get)

    payload = {
        'address': 'R. Prof. Eurico Rabelo',
        'city': 'Rio de Janeiro',
        'postalCode': 000000,
        'phoneNumber': 123,
    }

    # Call it the first time
    response = await async_client.post('/orders/address/validate', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Address is not in Portugal'}

    address_string = ' '.join([
        str(value) for key, value in payload.items() if key != 'phoneNumber'
    ]).strip()

    mock_get.assert_called_once_with(
        settings.GOOGLE_VALIDATION_API_URL,
        params={
            'address': address_string,
            'key': settings.GOOGLE_API_KEY,
        },
    )

    # Confirm that the value was cached in Redis
    cached_address = await redis_client.get(address_string)
    expiration_info = await redis_client.ttl(address_string)

    assert json.loads(cached_address) == {
        'is_validated': False,
        'message': 'Address is not in Portugal',
        'formatted_address': None,
    }
    assert expiration_info == settings.REDIS_EXPIRATION_TIME

    # Call it a second time
    response = await async_client.post('/orders/address/validate', json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Address is not in Portugal'}
