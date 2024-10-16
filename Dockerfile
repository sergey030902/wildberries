# Используем базовый образ Ubuntu
FROM ubuntu:20.04

# Устанавливаем часовой пояс (например, Europe/Moscow)
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    pkg-config \
    python3 \
    python3-pip \
    mysql-server \
    libmysqlclient-dev

# Копируем код приложения
COPY . /app
WORKDIR /app

# Устанавливаем Python-зависимости
RUN pip3 install -r requirements.txt

# Настраиваем MySQL
RUN service mysql start && \
    mysql -e "CREATE DATABASE std_2414_exam;" && \
    mysql -e "CREATE USER 'root'@'%' IDENTIFIED BY '12345';" && \
    mysql -e "GRANT ALL PRIVILEGES ON std_2414_exam.* TO 'root'@'%';" && \
    mysql -e "FLUSH PRIVILEGES;"

# Устанавливаем переменные окружения для Flask
ENV FLASK_APP=app/app.py
ENV FLASK_ENV=development

# Запускаем MySQL и Flask-приложение
CMD service mysql start && flask run --host=0.0.0.0

