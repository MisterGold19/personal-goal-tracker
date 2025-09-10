# Use bash for better error handling
SHELL := /usr/bin/env bash
.PHONY: install install-prod lock test fmt lint

# Instalacja wszystkiego do pracy lokalnej (runtime + dev)
install:
	poetry install --with dev

# Odświeżenie lockfile (zablokowanie wersji)
lock:
	poetry lock

# Szybkie testy
test:
	poetry run pytest -q

# Formatowanie i lint
fmt:
	poetry run black .
lint:
	poetry run ruff check .
