from .extension import db
from datetime import date
from flask_login import UserMixin
from werkzeug.security import check_password_hash



class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    description = db.Column(db.TEXT) # TEXT
    year = db.Column(db.INT) # YEAR
    publishing_house = db.Column(db.VARCHAR(100)) # VARCHAR
    author = db.Column(db.VARCHAR(100)) # VARCHAR
    pages = db.Column(db.INT) # INT
    cover = db.Column(db.INT, db.ForeignKey('covers.id')) # Внешний ключ

    reviews = db.relationship('Reviews', backref="books", uselist=True)
    genres = db.relationship('BooksAndGenres', backref="books", uselist=True)
    cover_image = db.relationship('Covers', backref="books", uselist=False)

    def __repr__(self):
        return f"<books {self.id}>"

class Covers(db.Model):
    __tablename__ = 'covers'

    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    mime_type = db.Column(db.VARCHAR(100)) # VARCHAR
    md5_hash = db.Column(db.VARCHAR(100)) # VARCHAR

    def __repr__(self):
        return f"<covers {self.id}>"

class Genres(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR(100)) # VARCHAR

    def __repr__(self):
        return f"<genres {self.id}>"

class BooksAndGenres(db.Model):
    __tablename__ = 'books_and_genres'

    id = db.Column(db.INT, primary_key=True)
    book = db.Column(db.INT, db.ForeignKey('books.id', ondelete='CASCADE')) # Внешний ключ
    genre =  db.Column(db.INT, db.ForeignKey('genres.id')) # Внешний ключ

    def __repr__(self):
        return f"<books_and_genres {self.id}>"

class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.INT, primary_key=True)
    book = db.Column(db.INT, db.ForeignKey('books.id', ondelete='CASCADE')) # Внешний ключ
    user = db.Column(db.INT, db.ForeignKey('users.id')) # Внешний ключ
    grade = db.Column(db.INT) # INT
    text = db.Column(db.TEXT) # TEXT
    date = db.Column(db.Date, default = date.today) # DATE
    status =  db.Column(db.INT, db.ForeignKey('statuses.id'), default = 1) # Внешний ключ

    book_info = db.relationship('Books', backref='reviewss', uselist=False)
    user_info = db.relationship('Users', backref='reviews', uselist=False)
    status_info = db.relationship('Statuses', backref='reviews', uselist=False)

    def __repr__(self):
        return f"<reviews {self.id}>"

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.INT, primary_key=True)
    login = db.Column(db.VARCHAR(100)) # VARCHAR
    password_hash = db.Column(db.VARCHAR(200)) # VARCHAR
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    surname = db.Column(db.VARCHAR(100)) # VARCHAR
    patronymic  = db.Column(db.VARCHAR(100)) # VARCHAR
    role = db.Column(db.INT, db.ForeignKey('roles.id')) # Внешний ключ

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        return self.role

    @property
    def full_name(self):
        return ' '.join([self.surname, self.name, self.patronymic or ''])

    @property
    def is_admin(self):
        return self.role == 1

    @property
    def is_moderator(self):
        return self.role == 2

    @property
    def is_user(self):
        return self.role == 3

    def __repr__(self):
        return f"<users {self.id}>"

class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR(100)) # VARCHAR
    text = db.Column(db.TEXT) # TEXT

    def __repr__(self):
        return f"<roles {self.id}>"

class Statuses(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.VARCHAR(100)) # VARCHAR

    def __repr__(self):
        return f"<statuses {self.id}>"
