from app import *
from config import *
import flask
with flask.app_context():
    db.create_all()
