
class Config:
    SECRET_KEY = 'b3baa1cb519a5651c472d1afa1b3f4e04f1adf6909dae88a4cd39adc0ddd9732'
    # SQLALCHEMY_DATABASE_URI = 'mysql:///std_2414_exam.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:55555@db:3306/std_2414_exam'
    UPLOAD_FOLDER = "./static/covers"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

