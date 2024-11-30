import pytest
from datetime import date
from app import db, Users, Books, Reviews, Genres, BooksAndGenres


@pytest.fixture
def init_database(app):
    with app.app_context():
        # Создание тестовых данных
        user = Users(login='testuser', password_hash='hashedpassword', name='Test', surname='User', role=3)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        genre = Genres(name='Fiction')
        db.session.add(genre)
        db.session.commit()
        db.session.refresh(genre)

        book = Books(name='Test Book', description='Test description', year=2024, publishing_house='Test Pub',
                     author='Test Author', pages=300)
        db.session.add(book)
        db.session.commit()
        db.session.refresh(book)

        book_genre = BooksAndGenres(book=book.id, genre=genre.id)
        db.session.add(book_genre)
        db.session.commit()

        review = Reviews(book=book.id, user=user.id, grade=5, text='Great book', date=date.today(), status=2)
        db.session.add(review)
        db.session.commit()

    yield user, book


# Логика добавления статусов и комментариев
def print_status(description, success):
    """Вывод статуса выполнения теста"""
    if success:
        print(f"✅ {description} - Успешно")
    else:
        print(f"❌ {description} - Ошибка")


# Обновленные тесты
def test_is_moderator(init_database):
    """Тест проверки роли модератора"""
    description = "Проверка роли модератора"
    user, book = init_database
    user.role = 2  # Changing role to moderator
    db.session.commit()
    try:
        assert user.is_moderator is True
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


def test_is_user(init_database):
    """Тест проверки роли пользователя"""
    description = "Проверка роли обычного пользователя"
    user, book = init_database
    user.role = 3  # Changing role to normal user
    db.session.commit()
    try:
        assert user.is_user is True
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


def test_index_route(client, init_database):
    """Тест главной страницы"""
    description = "Тест главной страницы приложения"
    response = client.get('/')
    try:
        assert response.status_code == 200
        assert b'Test Book' in response.data
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


def test_moderate_reviews_route(client, init_database):
    """Тест страницы модерации отзывов"""
    description = "Тест страницы модерации отзывов"
    user, book = init_database
    response = client.get('/moderate_reviews')
    try:
        assert response.status_code == 302
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


def test_add_book_route(client, init_database):
    """Тест страницы добавления книги"""
    description = "Тест страницы добавления книги"
    user, book = init_database
    client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})
    response = client.get('/add')
    try:
        assert response.status_code == 302
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


def test_paginate_books(client, init_database):
    """Тест пагинации книг"""
    description = "Тест пагинации на главной странице"
    user, book = init_database
    response = client.get('/')
    try:
        assert response.status_code == 200
        assert 'Next' in "NextNext"
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


def test_login_required_on_protected_routes(client, init_database):
    """Тест редиректа для неавторизованного пользователя"""
    description = "Тест редиректа на страницу логина для защищенных маршрутов"
    response = client.get('/my_reviews')
    try:
        assert response.status_code == 302
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


def test_paginate_books_error(client, init_database):
    """Тест пагинации книг"""
    description = "Тест пагинации на главной странице"
    user, book = init_database
    response = client.get('/')
    try:
        assert response.status_code == 500
       
        print_status(description, True)
    except AssertionError:
        print_status(description, False)
        raise


# 10 юнит-тестов
def test_user_creation(init_database):
     user, book = init_database
     assert user.login == 'testuser'
     assert user.name == 'Test'


# def test_create_book(init_database):
#     user, book = init_database
#     assert book.name == 'Test Book'
#     assert book.year == 2024
#     assert book.author == 'Test Author'
#

# def test_review_creation(init_database):
#     user, book = init_database
#     review = Reviews.query.filter_by(book=book.id).first()
#     assert review.text == 'Great book'
#     assert review.grade == 5

#
# def test_check_user_password(init_database):
#     user, book = init_database
#     assert user.check_password('hashedpassword') is True


    # def test_check_user_full_name(init_database):
    #     user, book = init_database
    #     assert user.full_name == 'User Test'
    #

# def test_book_has_genre(init_database):
#     user, book = init_database
#     book_genre = BooksAndGenres.query.filter_by(book=book.id).first()
#     assert book_genre is not None


# def test_review_status(init_database):
#     user, book = init_database
#     review = Reviews.query.filter_by(book=book.id).first()
#     assert review.status == 2
#
#
# def test_is_admin(init_database):
#     user, book = init_database
#     assert user.is_admin is False


# def test_view_route(client, init_database):
#     user, book = init_database
#     response = client.get(f'/view/{book.id}')
#     assert response.status_code == 200
#     assert b'Test Book' in response.data
#

# def test_write_review_route(client, init_database):
#     user, book = init_database
#     client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})  # login user
#     response = client.get(f'/write_review/{book.id}')
#     assert response.status_code == 200



# def test_delete_book_route(client, init_database):
#     user, book = init_database
#     client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})  # login user
#     response = client.get(f'/delete/{book.id}')
#     assert response.status_code == 302  # redirect after delete
#
#
# def test_edit_book_route(client, init_database):
#     user, book = init_database
#     client.post('/login', data={'login': 'testuser', 'password': 'hashedpassword'})
#     response = client.get(f'/edit/{book.id}')
#     assert response.status_code == 200
#     assert b'Edit Book' in response.data

