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

```bash
python3 -m pip install --user poetry
pip install poetry
poetry install
```

For dev tooling:
```poetry install --with dev```

### Docker setup

#### Environment configuration

Before running the container for the first time, copy the example environment file:

```bash
cp --update=none .env.example .env
```

In case you already have .env, parameter `-n` exists, so it's not overwriting your .env file (just for safe)

Build the image:

```bash
docker build -t pgt-api:dev .
```

Run the container (default port 8000):

```bash
docker run --rm -p 8000:8000 pgt-api:dev
```

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
