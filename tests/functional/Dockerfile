# pull official base image
FROM python:3.9.6-alpine as builder

RUN apk update \
    && apk add gcc python3-dev musl-dev rust cargo patchelf

RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install orjson

FROM python:3.9.6-alpine

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

RUN apk add --no-cache libstdc++
RUN apk add --no-cache build-base

# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /tests/functional
COPY requirements.txt .
RUN export PYTHONDONTWRITEBYTECODE=1 \
    && export PYTHONUNBUFFERED=1 \
    && pip install --upgrade pip && pip3 install --no-cache-dir -r /tests/functional/requirements.txt
COPY . /tests/functional
RUN chmod +x /tests/functional/entrypoint.sh
ENTRYPOINT ["/tests/functional/entrypoint.sh"]