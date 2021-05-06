FROM python:3.8-slim

COPY source/ /app/
COPY requirements.txt /app
RUN python -m pip install --upgrade pip && pip install -r /app/requirements.txt

WORKDIR /app
ENTRYPOINT exec python client_service.py \
    ${DB_URL:-"postgresql+asyncpg://postgres:postgres@postgres:5432/"} \
    ${REST_PORT:-8080} \
    ${REST_HOST:-"0.0.0.0"}