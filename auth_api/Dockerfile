# Образ, от которого идет наследование
FROM python:3.10
# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /app
# Устанавливаем зависимости 
COPY requirements.txt /app/
RUN export PYTHONDONTWRITEBYTECODE=1
RUN export PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt
# Добавляем внутрь образа папку с приложением 
ADD flauth /app/flauth
ADD entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
