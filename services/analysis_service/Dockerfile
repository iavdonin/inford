FROM python:3.8-slim

COPY source/ /app/
COPY requirements.txt /app
RUN python -m pip install --upgrade pip && pip install -r /app/requirements.txt

WORKDIR /app
ENTRYPOINT exec python analysis_service.py \
    ${REST_PORT:-5000} \
    ${REST_HOST:-"127.0.0.1"}
