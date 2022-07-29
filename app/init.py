from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .orm_settings import TORTOISE_ORM


def create_app() -> FastAPI:
    app = FastAPI()

    register_tortoise(app, config=TORTOISE_ORM)
    register_routers(app)

    return app


def register_routers(app: FastAPI):
    from .routers import tweet_router, user_router

    app.include_router(tweet_router)
    app.include_router(user_router)
