import json
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Cookie, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import select

from integrations import google_integration
from models import CheckoutSessionStatus, Orders, OrderStatus, PaymentStatus
from src.api.dependencies import RedisClient, SessionDep
from src.core.settings import settings
from src.integrations.stripe_integration import StripeClient
from src.schemas.integrations import AddressValidationSchema, ValidateAddressInfoRequest
from src.schemas.orders import (
    CreateCheckoutSessionPayload,
    PhotoDetails,
    PhotosUploadPayload,
)

stripe_client = StripeClient()

router = APIRouter()


@router.post('/upload/photos')
async def upload_photos(
    payload: PhotosUploadPayload,
    redis_client: RedisClient,
    session_id: str | None = Cookie(None),
) -> JSONResponse:
    """
    Stores the photos in Redis and generates a session ID to be stored as a cookie
    on the client-side.

    The session ID will be used as an identifier to retrieve the photos from Redis.
    """
    if session_id is None:
        session_id = str(uuid.uuid4())

    photos_json = json.dumps([photo.model_dump() for photo in payload.photos])

    await redis_client.set(session_id, photos_json)

    response = JSONResponse({'message': 'Successfully stored in Redis'})
    response.set_cookie(key='session_id', value=session_id, httponly=True)

    return response


@router.post('/address/validate')
async def validate_customer_address(
    payload: ValidateAddressInfoRequest, redis_client: RedisClient
) -> AddressValidationSchema:
    """
    Validates if the customer's provided address corresponds to a single location
    and if it is in Portugal.
    """
    address_info = payload.model_dump()

    address_string = ' '.join([
        str(value) for key, value in address_info.items() if key != 'phoneNumber'
    ]).strip()

    if await redis_client.exists(address_string):
        cached_address = await redis_client.get(address_string)
        address_validation = AddressValidationSchema(**json.loads(cached_address))
    else:
        address_validation = await google_integration.verify_address(address_string)
        cache_value = address_validation.model_dump_json()
        await redis_client.set(
            address_string, cache_value, ex=settings.REDIS_EXPIRATION_TIME
        )

    if not address_validation.is_validated:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=address_validation.message
        )

    return address_validation


@router.post('/checkout', response_model=str)
async def create_checkout_session(
    session: SessionDep,
    redis_client: RedisClient,
    payload: CreateCheckoutSessionPayload,
    session_id: str | None = Cookie(None),
) -> str:
    """
    Generates the Stripe checkout session and returns the URL for redirection.
    """
    if not session_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Session ID not found in cookies'
        )

    photos_info = await redis_client.get(session_id)
    photos_info = PhotosUploadPayload(
        photos=[PhotoDetails(**photo) for photo in json.loads(photos_info)]
    )

    total_photos = sum([photo.quantity for photo in photos_info.photos])

    customer = await stripe_client.get_customer_by_email(payload.customerEmail)

    if not customer:
        customer = await stripe_client.create_customer(payload.customerEmail)

    checkout_session = await stripe_client.create_checkout_session(
        quantity=total_photos, stripe_customer_id=customer['id']
    )

    async with session.begin():
        new_order = Orders(
            unit_amount=checkout_session['amount_total'],
            quantity=total_photos,
            order_status=OrderStatus.OPEN,
            payment_status=PaymentStatus.UNPAID,
            stripe_checkout_session_status=CheckoutSessionStatus.OPEN,
            stripe_checkout_session_id=checkout_session['id'],
            checkout_session_expires_at=checkout_session['expires_at'],
            stripe_checkout_session_url=checkout_session['url'],
            stripe_payment_link=checkout_session['payment_link'],
        )
        session.add(new_order)

    checkout_url = checkout_session.get('url')

    if not isinstance(checkout_url, str):
        raise

    return checkout_url


@router.get('/success/{checkout_session}', response_model=RedirectResponse)
async def process_payment_success(
    session: SessionDep, checkout_session: str
) -> RedirectResponse:
    """
    Process the photo storage after the payment is successfully confirmed.
    """
    order = await session.scalar(
        select(Orders).where(Orders.stripe_checkout_session_id == checkout_session)
    )

    if not order:
        return RedirectResponse('/payment/error', status_code=HTTPStatus.SEE_OTHER)

    stripe_checkout_session = await stripe_client.get_checkout_session(
        checkout_session=checkout_session
    )

    if (
        stripe_checkout_session.get('status') == 'complete'
        and stripe_checkout_session.get('payment_status') == 'paid'
    ):
        order.stripe_checkout_session_status = CheckoutSessionStatus.COMPLETE
        order.payment_status = PaymentStatus.PAID
        order.order_status = OrderStatus.PAID
    else:
        return RedirectResponse('/payment/error', status_code=HTTPStatus.SEE_OTHER)

    # process celery tasks here

    return RedirectResponse('/payment/success', status_code=HTTPStatus.SEE_OTHER)
