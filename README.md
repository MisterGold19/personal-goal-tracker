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

### Fresh setup (clean environment)

```bash
pip install poetry
poetry install
```

For dev tooling:
```poetry install --with dev```

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

- `make install` - install runtime + dev dependencies
- `make lock` - regenerate `poetry.lock`
- `make test` - run tests
- `make fmt` - format code (black)
- `make lint` - lint code(ruff)

## Contributing

Zasady pojawią się później
