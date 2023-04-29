from fastapi import FastAPI, APIRouter

from api.routes import ping, list
from deps import get_settings


def init_app(app: FastAPI) -> FastAPI:
    register_routes(app)
    return app


def register_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")
    router.include_router(router=ping.router)
    router.include_router(router=list.router)
    app.include_router(router=router)


settings = get_settings()
app = init_app(
    FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION
    )
)
