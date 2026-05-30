run:
    uvicorn src.main:app --host 127.0.0.1 --port 8080 --reload

test:
    pytest

lint:
    uv run ruff check .

format:
    uv run ruff format .

up:
    docker compose up --build

down:
    docker compose down

worker:
    uv run celery -A src.core.celery worker -l info --beat
