from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.crypto.router import router
from src.core.database import ping_database


def create_app() -> FastAPI:
    app = FastAPI(
        title="Crypto Client",
        version="1",
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
