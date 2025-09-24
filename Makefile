# Use bash for better error handling
SHELL := /usr/bin/env bash
.PHONY: install lock test cov fmt lint type run

help: ## Pokaż listę dostępnych komend
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk -F ':.*?## ' '{printf "%-15s %s\n", $$1, $$2}'

install: ## Instalacja wszystkiego do pracy lokalnej (runtime + dev)
	poetry install --with dev

lock: ## Odświeżenie lockfile (zablokowanie wersji)
	poetry lock

test: ## Szybkie testy
	poetry run pytest -q || [ $$? -eq 5 ]
# $? = komenda specjalna w bashu - kod wyjścia ostatnio uruchomionej komendy
# $$? = $ w makefile używa sie do zmiennych Make. Aby przekazać $ do shella trzeba podwoić $$
# -eq = equals, używa się do porównania liczb
# 5 = kod wyjscia pytest, jeśli nie ma testów
# [ ... ] = sprawdzenie warunku logicznego

cov: ## Testy z pokryciem
	poetry pytest --cov=app --cov-report=term-missing || [ $$? -eq 5 ]

fmt: ## Formatowanie
	poetry run black .
lint: ## Lint
	poetry run ruff check .

type: ## Sprawdzanie typów
	poetry run mypy --strict app

ready-to-commit: ## Prepare to comit
	make fmt && make lint && make type

run: # Uruchomienie aplikacji
	uvicorn app.main:app --reload

