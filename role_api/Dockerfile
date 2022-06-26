# Образ, от которого идет наследование
FROM python:3.10
# Рабочая директория для CMD и ENTRYPOINT
WORKDIR /auth_api/flauth
# Устанавливаем зависимости 
RUN ls
COPY /requirements.txt /auth_api/
RUN export PYTHONDONTWRITEBYTECODE=1 \
    && export PYTHONUNBUFFERED=1 \
    && pip install --upgrade pip && pip3 install --no-cache-dir -r /auth_api/requirements.txt
# Добавляем внутрь образа папку с приложением 
ADD ./flauth /auth_api/flauth
CMD ["python3", "wsgi_app.py"]
