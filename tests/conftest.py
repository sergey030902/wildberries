import pytest
from app import create_app, db, TestConfig
from app.models import Users, Books, Genres, BooksAndGenres, Reviews  # or any model you're using
from datetime import date

@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        # Ensure that any database modifications are rolled back after each test
        yield app
        db.session.remove()  # Ensure session is closed after tests
        db.drop_all()  # Drop all tables after each test


@pytest.fixture()
def client(app):
    return app.test_client()


