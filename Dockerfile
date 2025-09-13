# FROM python:3.12-alpine
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR=/tmp/poetry \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

# -eux = {-e=exit on errors, -u=unset vars are errs, -x=print commands}
# user group and user definitions
# install poetry as root

# version for python-slim
#always update + install + cleanup in one RUN

RUN set -eux; \
    apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists* \
    && groupadd -r appgroup \
    && useradd -r -g appgroup -m -d /home/appuser appuser \
    && pip install --upgrade pip poetry \
    && chown -R appuser:appgroup /app
# version for python-alpine
# RUN set -eux; \
#     addgroup -S appgroup && adduser -S -G appgroup -h /home/appuser appuser; \
#     pip install --upgrade pip poetry; \
#     chown -R appuser:appgroup /app

COPY --chown=appuser:appgroup pyproject.toml poetry.lock ./

#change user form root to appuser
USER appuser

RUN poetry install --no-root --no-interaction --no-ansi \
    && poetry run uvicorn --version

COPY --chown=appuser:appgroup . .

# RUN chown -R appuser:appgroup /app

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
