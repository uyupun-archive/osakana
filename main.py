import uvicorn
from fastapi import FastAPI, APIRouter

from api.routes import ping, reading_list
from deps import get_global_settings
from settings import Settings


def init_app(settings: Settings=get_global_settings()) -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION
    )
    register_routes(app)
    return app


def register_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")
    router.include_router(router=ping.router)
    router.include_router(router=reading_list.router)
    app.include_router(router=router)


app = init_app()


if __name__ == "__main__":
    settings = get_global_settings()
    uvicorn.run("main:app", host=settings.ADDRESS, port=settings.PORT, reload=True)
