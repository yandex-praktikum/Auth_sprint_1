# Образ, от которого идет наследование
FROM python:3.10.3-alpine as builder
# Рабочая директория для CMD и ENTRYPOINT

RUN apk add alpine-sdk

RUN apk update \
    && apk add build-base g++ postgresql-dev gcc python3-dev musl-dev libffi-dev

RUN apk add postgresql-client


# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /app/
# Устанавливаем зависимости 
COPY requirements.txt /app/
RUN export PYTHONDONTWRITEBYTECODE=1
RUN export PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt
COPY . /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]