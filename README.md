# Personal Goals Tracker

## Overview

### Executive Summary

Celem projektu jest stowrzenie aplikacji webowej typu backend API,
służąca do śledzenia i raportowania celów uzytkownika.

Pierwsza wersja (MVP) planowo ma obejmować:

- moduł Goals
- podstawowe raporty o postępach
- pełną konteneryzację (Docker + docker-compose)
- CI/CD (GitHub actions)

Planowo system ma być rozszerzalny na kolejne moduły, oparty na Pythonie

### Motywacja

Projekt planowo jest kombinacją nauki narzędzi takich jak

- Docker desktop
- Git
- Postman
- Ubuntu
- Python

ale również ma służyć autorowi w celach osobistych

## Stack

(planowany)

- Python 3.12
- FastAPI
- Docker & Docker Compose
- PostgreSQL (planowane)
- VS Code (zalecane IDE)
- Postman

## Status

Projekt jest w fazie początkowej

## Roadmap

- [ ] Setup
- [ ] Goals CRUD
- [ ] Reports
- [ ] Deployment & Docs

## Dependencies

I use **Poetry** for dependency management and locking

### Runtime

- fastapi
- uvicorn[standard]
- pydantic>=2
- sqlalchemy>=2
- alembic
- psycopg[binary]
- python-dotenv
- structlog
- prometheus-client

### Dev

- pytest
- pytest-asyncio
- httpx
- mypy
- ruff
- black
- types-requests

## Quickstart

### Local setup (Poetry)

Fresh setup (clean environment)

Make sure Poetry is installed globally.
On Ubuntu/Debian you can install it via:

```bash
sudo apt install python3-poetry
```

Check installation:

```bash
poetry --version
```

For dev tooling:
```poetry install --with dev```

As a developer you can add a new package via

```bash
poetry add < package_name >
```

Poetry will automatically create a virtual environment in the project folder (`.venv/`).
You don’t need to activate it manually – use `poetry run ...` or the provided Makefile targets.

Use `poetry shell` before running scripts.

### Docker setup

#### Environment configuration

Before running the container for the first time, copy the example environment file:

```bash
cp --update=none .env.example .env
```

In case you already have .env, parameter `-n` exists, so it's not overwriting your .env file (just for safe)

Build the image and run containers:

```bash
docker compose up --build
```

To check in env was read:

```bash
docker compose config
```

### Environment Variables

The application uses the following environment variables (loaded automatically from .env or passed via Docker Compose):

| Variable          | Description                                      | Defined manually or in `.env.example` |
|-------------------|--------------------------------------------------|----------------------------------------|
| `POSTGRES_USER`     | PostgreSQL username                              | Manually                               |
| `POSTGRES_PASSWORD` | PostgreSQL password                              | Manually                               |
| `POSTGRES_DB`       | PostgreSQL database name                         | Manually                               |
| `ENV`               | Environment mode (`dev`, `prod`, …)              | `.env.example`                         |
| `APP_VERSION`       | Application version string, exposed in `/health` | `.env.example`                         |
| `LOG_LEVEL`         | Logging level                                    | `.env.example`                         |
| `DATABASE_URL`      | PostgreSQL connection string (used by the app)   | `.env.example`                         |

### Verify installation

After installation, run:

```bash
poetry run python -c "import fastapi, sqlalchemy, alembic"
```

this should exit with `0`

### Lockfile

The repository includes a `poetry.lock` file which pins exact versions.
To refresh the lockfile, run:

```bash
poetry lock
```

### Makefile

Common comands:

- `make help` - show list of comands
- `make install` - install runtime + dev dependencies
- `make lock` - regenerate `poetry.lock`
- `make test` - run tests
- `make cov` - run tests with coverage
- `make fmt` - format code (black)
- `make lint` - lint code(ruff)
- `make type` - check the types
- `make ready-to-commit` - run make fmt, lint and type
- `make run` - run the application

## Contributing

Zasady pojawią się później
