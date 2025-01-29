from typing import Any, TypeAlias, cast

import stripe

from src.core.settings import settings

TypeCasted: TypeAlias = list[dict[str, Any]]


class StripeClient:
    def __init__(self) -> None:
        stripe.api_key = settings.STRIPE_API_KEY

    @classmethod
    async def get_customers(cls) -> TypeCasted:
        customer_list = await stripe.Customer.list_async(limit=100)

        return cast(TypeCasted, customer_list['data'])

    @classmethod
    async def get_customer_by_email(cls, email: str) -> dict[str, Any] | None:
        search_query = f"email:'{email}'"

        customer = await stripe.Customer.search_async(query=search_query)

        customer_info = customer.get('data')

        if not customer_info:
            return None

        return cast(dict[str, Any], customer_info[0])

    @classmethod
    async def create_customer(cls, customer_email: str) -> dict[str, Any]:
        new_customer = await stripe.Customer.create_async(
            email=customer_email,
        )

        return new_customer

    @classmethod
    async def create_checkout_session(
        cls, quantity: int, stripe_customer_id: str
    ) -> dict[str, Any]:
        checkout_session = await stripe.checkout.Session.create_async(
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': quantity,
                },
            ],
            customer=stripe_customer_id,
            mode='payment',
            success_url=(
                settings.BACKEND_DOMAIN + '/orders/success/{CHECKOUT_SESSION_ID}'
            ),
            cancel_url=(settings.BACKEND_DOMAIN + '/order/fail'),
        )

        return checkout_session

    @classmethod
    async def get_checkout_session(cls, checkout_session: str) -> dict[str, Any]:
        session = await stripe.checkout.Session.retrieve_async(checkout_session)

        return session

    @classmethod
    async def get_price_unit_amount(cls, stripe_price_id: str) -> int:
        price = await stripe.Price.retrieve_async(stripe_price_id)

        unit_amount = price['unit_amount']

        return cast(int, unit_amount)


stripe_client = StripeClient()
