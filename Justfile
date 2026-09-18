run:
    uv run uvicorn src.main:app --host 127.0.0.1 --port 8080 --reload

test:
    uv run pytest

lint:
    uv run ruff check .

format:
    uv run ruff format .

up:
    docker compose up --build

down:
    docker compose down

worker:
    uv run taskiq worker src.core.broker:broker src.crypto.tasks

scheduler:
    uv run taskiq scheduler src.core.broker:scheduler src.crypto.tasks
