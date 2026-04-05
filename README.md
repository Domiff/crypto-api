# Crypto Price Tracker — Backend

A **Deribit** client and **FastAPI** service for cryptocurrency **index prices**. A **Celery** worker (with embedded beat) polls `BTC_USD` and `ETH_USD` every minute and stores ticker, price, and UNIX timestamp in **PostgreSQL**. The API exposes read-only endpoints with a mandatory `ticker` query parameter.

## Features

- **Price polling**: scheduled fetch of Deribit index prices for configured instruments; persistence to PostgreSQL.
- **API**: list all rows for a ticker, get the latest price, filter by `start_date` / `end_date`.
- **Stack**: async SQLAlchemy + asyncpg, aiohttp for Deribit, RabbitMQ as the Celery broker.

## Tech stack

| Layer          | Technologies                                              |
| -------------- | --------------------------------------------------------- |
| API            | FastAPI, Uvicorn                                          |
| Data           | PostgreSQL, SQLAlchemy 2 (async), Alembic                 |
| Integration    | aiohttp (Deribit REST)                                    |
| Background     | Celery (worker + beat), RabbitMQ                          |
| Tooling        | uv, Ruff, pytest (async)                                  |
| Infrastructure | Docker, Docker Compose                                    |

## Application structure

### Architecture

```mermaid
flowchart TB
    subgraph external["External"]
        DR[Deribit API]
    end

    subgraph workers["Background"]
        CW[Celery worker + beat]
        RMQ[(RabbitMQ — broker)]
        CW <--> RMQ
    end

    subgraph api_layer["API"]
        F[FastAPI]
    end

    subgraph data["Data"]
        PG[(PostgreSQL)]
    end

    CW -->|aiohttp| DR
    CW --> PG
    F --> PG
    Clients([HTTP clients]) --> F
```

### Repository tree

```text
.
├── alembic/
│   ├── env.py                      # Alembic env (async engine)
│   ├── script.py.mako
│   └── versions/                   # Revision scripts
├── src/
│   ├── main.py                     # FastAPI app, CORS, router mount
│   ├── api/
│   │   ├── annotations.py        # Query types (ticker, dates)
│   │   ├── router.py             # GET routes
│   │   └── service.py            # Read-side queries
│   ├── client/
│   │   ├── crypto_client.py      # Deribit HTTP client
│   │   ├── service.py            # Fetch + persist prices
│   │   ├── tasks.py              # Celery tasks / schedule
│   │   └── urls.py               # Deribit URL helpers
│   ├── database/
│   │   ├── connection.py         # Async session dependency
│   │   └── models.py
│   └── settings/
│       ├── celery_app.py
│       └── config.py             # Pydantic settings from env
├── tests/
│   ├── conftest.py
│   └── tests.py
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── pytest.ini
└── uv.lock
```

## Requirements

- **Python 3.14+** (see `pyproject.toml`)
- **[uv](https://docs.astral.sh/uv/)** (recommended) for installs
- **Docker** / Docker Compose for Postgres, RabbitMQ, API, and Celery

## Configuration

Create **`.env`** at the **repository root** (gitignored; do not commit secrets). Copy from `.env_template` and fill values.

| Variable | Purpose |
| -------- | ------- |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | PostgreSQL database and credentials |
| `POSTGRES_HOST`, `POSTGRES_PORT` | e.g. `pg` and `5432` in Compose; `127.0.0.1` when Postgres runs on the host |
| `BASE_URL`, `BTC`, `ETH` | Deribit-related settings (see `src/settings/config.py` / client code) |
| `CELERY_BROKER_URL` | Celery broker, e.g. `amqp://user:pass@rabbitmq:5672//` in Compose |
| `RABBITMQ_DEFAULT_USER`, `RABBITMQ_DEFAULT_PASS` | RabbitMQ credentials (used by the `rabbitmq` service) |

## Local development (without full Compose)

1. Install dependencies:
   ```bash
   uv sync --group dev
   ```
2. Run **PostgreSQL** and **RabbitMQ** locally or via Docker, set `.env` accordingly.
3. Apply migrations:
   ```bash
   uv run alembic upgrade head
   ```
4. Start the API:
   ```bash
   uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
   ```
5. Start Celery (from repo root; broker must match `CELERY_BROKER_URL`):
   ```bash
   uv run celery -A src.settings.celery_app worker -l info --beat
   ```

## Docker Compose

From the repository root:

```bash
docker compose up --build
```

Apply migrations after containers are up:

```bash
docker compose exec api alembic upgrade head
```

Typical ports:

| Service   | Port  | Notes                    |
| --------- | ----- | ------------------------ |
| API       | 8080  | Uvicorn (`src.main:app`) |
| Postgres  | 5432  | Volume `pgdata`          |
| RabbitMQ  | 5672  | AMQP                     |
| RabbitMQ UI | 15672 | Management plugin      |

## API overview

All read routes use **GET** and a required query parameter **`ticker`** (`btc` or `eth`, see `src/api/annotations.py`).

| Route | Query parameters | Purpose |
| ----- | ---------------- | ------- |
| `/crypto` | `ticker` | All stored rows for the ticker |
| `/last-price` | `ticker` | Latest price |
| `/date-filter` | `ticker`, `start_date`, `end_date` | Rows in the datetime range |

Interactive documentation:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

CORS is configured for Vite dev origins (`http://localhost:5173`, `http://127.0.0.1:5173`); extend `origins` in `src/main.py` if needed.

## Development tooling

- **Ruff**: `uv run ruff check` (see `pyproject.toml`)
- **Tests**: `uv run pytest`
