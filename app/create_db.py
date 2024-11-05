from app import app  # Импортируйте объект приложения
from config import *  # Если требуется, импортируйте конфигурацию
from app import db    # Импортируйте объект базы данных, если нужно

with app.app_context():  # Используйте контекст вашего приложения
    db.create_all()  # Создание всех таблиц
