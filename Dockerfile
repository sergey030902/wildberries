# Используем базовый образ Python
FROM python:3.10.12

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y pipenv pkg-config default-libmysqlclient-dev

# Копируем код приложения
COPY . /app
WORKDIR /app

# Устанавливаем зависимости из requirements.txt
RUN pipenv install -r requirements.txt

# Устанавливаем переменные окружения для Flask
RUN pipenv run flask db init && pipenv run flask db migrate -m "Initial migration." && pipenv run flask db upgrade

# Запускаем MySQL и Flask-приложение
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]

