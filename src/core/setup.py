from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.database import ping_database
from src.crypto.router import router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app.APP_TITLE,
        version=settings.app.APP_VERSION,
    )

    setup_middlewares(app)
    setup_healthcheck(app)
    app.include_router(router)

    return app


def setup_middlewares(app: FastAPI) -> None:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_healthcheck(app: FastAPI) -> None:
    @app.get("/health", tags=["health"])
    async def health() -> bool:
        return await ping_database()
