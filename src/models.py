import enum
from datetime import datetime

from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class OrderStatus(enum.Enum):
    OPEN = 'open'
    PAID = 'paid'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'


class PaymentStatus(enum.Enum):
    PAID = 'paid'
    UNPAID = 'unpaid'


class CheckoutSessionStatus(enum.Enum):
    OPEN = 'open'
    COMPLETE = 'complete'
    EXPIRED = 'expired'


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_email: Mapped[str]
    customer_phone_number: Mapped[str]
    delivery_address: Mapped[str]
    unit_amount: Mapped[int]
    quantity: Mapped[int]
    redis_cookie_session_id: Mapped[str]
    order_status: Mapped[OrderStatus] = mapped_column(SQLAlchemyEnum(OrderStatus))
    payment_status: Mapped[PaymentStatus] = mapped_column(SQLAlchemyEnum(PaymentStatus))
    stripe_checkout_session_status: Mapped[CheckoutSessionStatus] = mapped_column(
        SQLAlchemyEnum(CheckoutSessionStatus)
    )
    stripe_checkout_session_id: Mapped[str] = mapped_column(unique=True)
    checkout_session_expires_at: Mapped[int]
    stripe_checkout_session_url: Mapped[str] = mapped_column(
        default=None, nullable=True
    )
    stripe_payment_link: Mapped[str] = mapped_column(default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
