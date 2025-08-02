FROM python:3.13 AS base

WORKDIR /app

ENV PYTHONPATH=/app/src

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false 

RUN poetry config virtualenvs.in-project false

RUN poetry install --no-interaction --no-root

COPY .env /app/.env
COPY .gitignore /app/.gitignore
COPY ./alembic /app/alembic
COPY ./src /app/src
COPY ./alembic.ini /app/alembic.ini
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

RUN chmod +x /app/entrypoint.sh


FROM base AS server


ENTRYPOINT [ "/app/entrypoint.sh" ]