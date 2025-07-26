FROM python:3.13 AS base

WORKDIR /app

ENV PYTHONPATH=/app/src

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .

RUN chmod +x /app/entrypoint.sh


FROM base AS server


ENTRYPOINT [ "/app/entrypoint.sh" ]