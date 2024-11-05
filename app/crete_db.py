from app import *
from config import *
with app.app_context():
    db.create_all()