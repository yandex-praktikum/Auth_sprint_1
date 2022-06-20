# Образ, от которого идет наследование
FROM python:3.10
# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /core
ENV PYTHONPATH "${PYTHONPATH}:/core/"
# Устанавливаем зависимости 
COPY requirements.txt .
RUN export PYTHONDONTWRITEBYTECODE=1 \
    && export PYTHONUNBUFFERED=1 \
    && pip install --upgrade pip && pip3 install --no-cache-dir -r ./requirements.txt
COPY ./core /core

