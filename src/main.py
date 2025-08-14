from app.config import settings
from app.api import demo
from fastapi import FastAPI
from app.utils import exceptions
from app.utils.exceptions import BaseAPIException

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="FastAPI Demo with JSON & Form endpoints",
    )

    # 路由注册
    app.include_router(demo.router, prefix="/api")


    # 注册异常处理
    app.add_exception_handler(BaseAPIException, exceptions.base_api_exception_handler)
    app.add_exception_handler(Exception, exceptions.global_exception_handler)

    return app

app = create_app()
