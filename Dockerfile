FROM python:3.12-slim

# Привязываем образ к вашему репозиторию на GitHub автоматически
LABEL org.opencontainers.image.source=https://github.com/leckoy/django_docker

# Запрещаем Python создавать файлы кэша .pyc и включаем немедленный вывод логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ваш существующий код Django в контейнер
COPY . .

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]