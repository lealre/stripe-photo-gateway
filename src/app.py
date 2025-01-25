import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.dependencies import RedisClient
from src.core.database import engine
from src.models import Base
from src.schemas import PhotosUploadPostBodyRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.mount('/static', app=StaticFiles(directory='src/pages/static'), name='static')

templates = Jinja2Templates(directory='src/pages/templates')


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name='upload_photos.html')


@app.get('/order/details', response_class=HTMLResponse)
def order_details(request: Request):
    return templates.TemplateResponse(request=request, name='order_details.html')


@app.post('/upload')
async def upload_photos(
    payload: PhotosUploadPostBodyRequest, redis_client: RedisClient
):
    """
    Stores photos in redis
    """
    photos_json = json.dumps([photo.model_dump_json() for photo in payload.photos])

    await redis_client.set('photos', photos_json)

    return {'message': 'Stored in redis'}
