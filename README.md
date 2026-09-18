# Crypto Price Tracker — Backend

A **Deribit** client and **FastAPI** service for cryptocurrency **index prices**. A **taskiq** scheduler enqueues a price fetch every `INTERVAL` seconds (60 by default), a taskiq worker pulls the `BTC-PERPETUAL` and `ETH-PERPETUAL` tickers from Deribit and stores ticker, price, instrument name and load date in **PostgreSQL**. **Redis** is the task broker. The API exposes read-only endpoints with a mandatory `ticker` query parameter.

## Features

- **Price polling**: scheduled fetch of Deribit index prices; every row is stored with its ticker (`btc`, `eth`, …) and a `created_at` load date set by the database.
- **Retries**: a failed fetch is retried `TASKIQ_RETRY_COUNT` times; retries are delayed through a Redis schedule source, so they fire at the start of a following minute.
- **API**: list all rows for a ticker, get the latest price, filter by `start_date` / `end_date`, health check.
- **Stack**: async SQLAlchemy + asyncpg, aiohttp for Deribit, taskiq with Redis as the broker.

## Tech stack

| Layer          | Technologies                                        |
| -------------- | --------------------------------------------------- |
| API            | FastAPI, Uvicorn                                    |
| Data           | PostgreSQL (SQLite in debug mode), SQLAlchemy 2 (async), Alembic |
| Integration    | aiohttp (Deribit REST)                              |
| Background     | taskiq (worker + scheduler), Redis                  |
| Tooling        | uv, Ruff, pre-commit, pytest (async), just          |
| Infrastructure | Docker, Docker Compose                              |

## Application structure

```text
.
├── alembic/
│   ├── env.py                  # Alembic env (async engine)
│   ├── script.py.mako
│   └── versions/               # Revision scripts
├── src/
│   ├── main.py                 # Entry point: builds the app
│   ├── core/
│   │   ├── broker.py           # taskiq broker (Redis) and scheduler
│   │   ├── config.py           # Pydantic settings grouped by app/db/redis/crypto/taskiq
│   │   ├── database.py         # Async engine, session dependency, DB ping
│   │   ├── http.py             # Deribit HTTP client
│   │   ├── models.py           # Declarative base
│   │   └── setup.py            # App factory: CORS, health check, routers
│   └── crypto/
│       ├── models.py           # CryptoCurrency model
│       ├── repository.py       # Read and write queries
│       ├── router.py           # GET routes
│       └── tasks.py            # taskiq tasks and their schedule
├── tests/
│   ├── conftest.py             # In-memory SQLite fixtures
│   └── tests.py
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── Justfile
├── pyproject.toml
├── pytest.ini
└── uv.lock
```

## Data model

All coins live in one table, `crypto_currencies`:

| Column | Type | Notes |
| ------ | ---- | ----- |
| `id` | integer | Primary key |
| `ticker` | string | `btc`, `eth`, …; indexed |
| `index_price` | float | Deribit index price |
| `instrument_name` | string | e.g. `BTC-PERPETUAL` |
| `created_at` | datetime (tz) | Load date, set by the database |

Adding a new coin needs no schema change: add it to `INSTRUMENTS` in `src/crypto/tasks.py` and to `TickerQuery` in `src/crypto/router.py`.

## Requirements

- **Python 3.14+** (see `pyproject.toml`)
- **[uv](https://docs.astral.sh/uv/)** for installs
- **Redis** for the task broker
- **Docker** / Docker Compose for Postgres, Redis, API, worker and scheduler

## Configuration

Create **`.env`** at the **repository root** (gitignored; do not commit secrets). Copy from `.env_template` and fill values.

| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `IS_DEBUG` | `true` | `true`: local SQLite (`db.sqlite3`) and Redis on `localhost`; `false`: PostgreSQL and Redis at host `redis` |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | — | PostgreSQL database and credentials |
| `POSTGRES_HOST`, `POSTGRES_PORT` | `localhost`, `5432` | e.g. `pg` in Compose |
| `URL` | **required** | Deribit API base URL with a trailing slash, e.g. `https://www.deribit.com/api/v2/public/` |
| `INTERVAL` | `60` | How often prices are fetched, seconds |
| `REDIS_PORT`, `REDIS_DB` | `6379`, `0` | Redis port and database; the host follows `IS_DEBUG` |
| `CONNECTION_POOL_MAXSIZE` | `10` | Redis connection pool size |
| `EXPIRE` | `3600` | Reserved for Redis key expiry, seconds; not used yet |
| `TASKIQ_RETRY_COUNT`, `TASKIQ_RETRY_DELAY` | `5`, `10` | Retries for failed tasks and delay between them, seconds |
| `APP_TITLE`, `APP_VERSION` | `CryptoAPI`, `1` | Shown in the OpenAPI docs |

## Local development (without full Compose)

1. Install dependencies:
   ```bash
   uv sync --group dev
   ```
2. Run **Redis** (and **PostgreSQL** if `IS_DEBUG=false`) locally or via Docker, set `.env` accordingly.
3. Apply migrations:
   ```bash
   uv run alembic upgrade head
   ```
4. Start the API:
   ```bash
   uv run uvicorn src.main:app --reload --host 127.0.0.1 --port 8080
   ```
5. Start the taskiq worker, which executes tasks:
   ```bash
   uv run taskiq worker src.core.broker:broker src.crypto.tasks
   ```
6. Start the taskiq scheduler, which enqueues tasks on schedule:
   ```bash
   uv run taskiq scheduler src.core.broker:scheduler src.crypto.tasks
   ```

Run the scheduler as a **single instance**: two schedulers enqueue every task twice. Workers can be scaled freely.

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

| Service  | Port | Notes                    |
| -------- | ---- | ------------------------ |
| API      | 8080 | Uvicorn (`src.main:app`) |
| Postgres | 5432 | Volume `pgdata`          |
| Redis    | —    | taskiq broker; internal only, not published |

## API overview

All data routes use **GET** and a required query parameter **`ticker`** (`btc` or `eth`, see `src/crypto/router.py`).

| Route | Query parameters | Purpose |
| ----- | ---------------- | ------- |
| `/crypto` | `ticker` | All stored rows for the ticker |
| `/last-price` | `ticker` | Latest price; `404` if there is no data |
| `/date-filter` | `ticker`, `start_date`, `end_date` | Rows loaded within the datetime range |
| `/health` | — | `true` if the database is reachable |

Interactive documentation:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

CORS is configured for Vite dev origins (`http://localhost:5173`, `http://127.0.0.1:5173`); extend `origins` in `src/core/setup.py` if needed.

## Development tooling

Common commands are in the `Justfile` (`just run`, `just worker`, `just scheduler`, `just test`, `just lint`, `just format`, `just up`, `just down`), or run them directly:

- **Ruff**: `uv run ruff check` and `uv run ruff format` (see `pyproject.toml`)
- **Tests**: `uv run pytest` (in-memory SQLite, no external services needed)
- **pre-commit**: `uv run pre-commit install` to run Ruff on every commit
