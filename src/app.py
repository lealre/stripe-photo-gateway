from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.orders import router
from src.core.database import engine
from src.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.mount('/static', app=StaticFiles(directory='src/pages/static'), name='static')

app.include_router(router, prefix='/orders', tags=['orders'])

templates = Jinja2Templates(directory='src/pages/templates')


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name='upload_photos.html')


@app.get('/order/details', response_class=HTMLResponse)
def order_details(request: Request):
    return templates.TemplateResponse(request=request, name='order_details.html')
