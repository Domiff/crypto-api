from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.router import router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Crypto Client",
        version="1",
        lifespan=lifespan,
    )

    setup_middlewares(app)
    setup_healthcheck(app)
    app.include_router(router, tags=["crypto"])

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
        return True
