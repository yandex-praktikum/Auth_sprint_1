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

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy project
COPY . .

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]