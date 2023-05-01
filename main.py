import uvicorn
from fastapi import FastAPI, APIRouter

from api.routes import ping, reading_list
from settings import Settings


def init_app(settings: Settings=Settings.get_settings()) -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION
    )
    return app


def register_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")
    router.include_router(router=ping.router)
    router.include_router(router=reading_list.router)
    app.include_router(router=router)


def run_app(app: FastAPI, settings: Settings=Settings.get_settings()) -> None:
    uvicorn.run("main:app", host=settings.ADDRESS, port=settings.PORT, reload=True)


app = init_app()
register_routes(app=app)


if __name__ == "__main__":
    run_app(app=app)
