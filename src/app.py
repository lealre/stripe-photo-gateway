from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.orders import router
from src.core.database import engine
from src.core.settings import settings
from src.integrations.stripe_integration import stripe_client
from src.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # pragma: no cover
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.mount('/static', app=StaticFiles(directory='src/pages/static'), name='static')

app.include_router(router, prefix='/orders', tags=['orders'])

templates = Jinja2Templates(directory='src/pages/templates')


@app.get('/', response_class=HTMLResponse)
async def upload_photos_page(request: Request) -> HTMLResponse:
    unit_price = await stripe_client.get_price_unit_amount(
        stripe_price_id=settings.STRIPE_PRICE_ID
    )

    return templates.TemplateResponse(
        request=request,
        name='upload_photos.html',
        context={'unit_price': unit_price / 100},
    )


@app.get('/order/details', response_class=HTMLResponse)
async def order_details_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name='order_details.html')


@app.get('/payment/success', response_class=HTMLResponse)
async def payment_success_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name='payment_success.html')


@app.get('/payment/error', response_class=HTMLResponse)
async def payment_error_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name='payment_error.html')


@app.get('/error', response_class=HTMLResponse)
async def error_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name='error.html')
