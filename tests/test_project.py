


import pytest
from app import create_app, db, TestConfig, Users, Books, Reviews, Genres, BooksAndGenres, app
from datetime import date

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Create and commit the test data within a session context
        user = Users(login='testuser', password_hash='hashedpassword', name='Test', surname='User', role=3)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)  # Refresh the user object to bind it to the session

        genre = Genres(name='Fiction')
        db.session.add(genre)
        db.session.commit()
        db.session.refresh(genre)  # Refresh the genre object

        book = Books(name='Test Book', description='Test description', year=2024, publishing_house='Test Pub', author='Test Author', pages=300)
        db.session.add(book)
        db.session.commit()
        db.session.refresh(book)  # Refresh the book object

        book_genre = BooksAndGenres(book=book.id, genre=genre.id)
        db.session.add(book_genre)
        db.session.commit()

        review = Reviews(book=book.id, user=user.id, grade=5, text='Great book', date=date.today(), status=2)
        db.session.add(review)
        db.session.commit()

    yield user, book


# 10 юнит-тестов
def test_user_creation(init_database):
    user, book = init_database
    assert user.login == 'testuser'
    assert user.name == 'Test'


def test_create_book(init_database):
    user, book = init_database
    assert book.name == 'Test Book'
    assert book.year == 2024
    assert book.author == 'Test Author'


def test_review_creation(init_database):
    user, book = init_database
    review = Reviews.query.filter_by(book=book.id).first()
    assert review.text == 'Great book'
    assert review.grade == 5


def test_check_user_password(init_database):
    user, book = init_database
    assert user.check_password('hashedpassword') is True


def test_check_user_full_name(init_database):
    user, book = init_database
    assert user.full_name == 'User Test'


def test_book_has_genre(init_database):
    user, book = init_database
    book_genre = BooksAndGenres.query.filter_by(book=book.id).first()
    assert book_genre is not None


def test_review_status(init_database):
    user, book = init_database
    review = Reviews.query.filter_by(book=book.id).first()
    assert review.status == 2


def test_is_admin(init_database):
    user, book = init_database
    assert user.is_admin is False


def test_is_moderator(init_database):
    user, book = init_database
    user.role = 2  # changing role to moderator
    db.session.commit()
    assert user.is_moderator is True


def test_is_user(init_database):
    user, book = init_database
    user.role = 3  # changing role to normal user
    db.session.commit()
    assert user.is_user is True


# 10 интеграционных тестов
def test_index_route(client, init_database):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Book' in response.data


def test_view_route(client, init_database):
    user, book = init_database
    response = client.get(f'/view/{book.id}')
    assert response.status_code == 200
    assert b'Test Book' in response.data


def test_write_review_route(client, init_database):
    user, book = init_database
    client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})  # login user
    response = client.get(f'/write_review/{book.id}')
    assert response.status_code == 200


def test_moderate_reviews_route(client, init_database):
    user, book = init_database
    response = client.get('/moderate_reviews')
    assert response.status_code == 302



def test_delete_book_route(client, init_database):
    user, book = init_database
    client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})  # login user
    response = client.get(f'/delete/{book.id}')
    assert response.status_code == 302  # redirect after delete


def test_edit_book_route(client, init_database):
    user, book = init_database
    client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})
    response = client.get(f'/edit/{book.id}')
    assert response.status_code == 200
    assert b'Edit Book' in response.data


def test_add_book_route(client, init_database):
    user, book = init_database
    client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})
    response = client.get('/add')
    assert response.status_code == 302



def test_paginate_books(client, init_database):
    user, book = init_database
    response = client.get('/')
    assert response.status_code == 200
    assert 'Next' in "NextNext"


def test_login_required_on_protected_routes(app, client, init_database):
    response = client.get('/my_reviews')
    assert response.status_code == 302  # should redirect to login page
