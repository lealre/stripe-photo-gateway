from http import HTTPStatus
from unittest.mock import AsyncMock

import pytest
import stripe
from httpx import AsyncClient
from pytest_mock import MockerFixture

from src.core.settings import settings


async def test_upload_photos_page(
    async_client: AsyncClient, mocker: MockerFixture
) -> None:
    test_price = 5000
    expected_price_text = f'Unit Price: ${test_price / 100:.1f}'

    stripe_price_return = {'unit_amount': test_price, 'some_other_filed': 'test-field'}

    mock_get_price = mocker.patch.object(
        stripe.Price, 'retrieve_async', new=AsyncMock(return_value=stripe_price_return)
    )

    response = await async_client.get('/')

    mock_get_price.assert_called_once_with(settings.STRIPE_PRICE_ID)

    assert response.status_code == HTTPStatus.OK
    assert expected_price_text in response.text


@pytest.mark.parametrize(
    'endpoint', ['/order/details', '/payment/success', '/payment/error', '/error']
)
async def test_page_response_ok(async_client: AsyncClient, endpoint: str) -> None:
    response = await async_client.get(endpoint)
    assert response.status_code == HTTPStatus.OK
