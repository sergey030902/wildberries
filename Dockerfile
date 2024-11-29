# Используем базовый образ Python
FROM python:3.10.12

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y pipenv pkg-config default-libmysqlclient-dev iputils-ping

# Копируем код приложения
COPY . /app
WORKDIR ./app

# Устанавливаем зависимости из requirements.txt

RUN pipenv install ../Pipfile
RUN pipenv install pytest

WORKDIR ./app

# Устанавливаем переменные окружения для Flask

# Запускаем MySQL и Flask-приложение
ENV PYTHONPATH=/app

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]

