FROM python:3.8-slim

COPY source/ /app/
COPY requirements.txt /app
RUN python -m pip install --upgrade pip && pip install -r /app/requirements.txt

WORKDIR /app
ENTRYPOINT exec python data_service.py \
    ${DB_URL:-"postgresql+asyncpg://postgres:postgres@localhost/inford_db"} \
    ${REST_PORT:-5000} \
    ${REST_HOST:-"127.0.0.1"}
