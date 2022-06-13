import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    WTF_CSRF_SECRET_KEY = 'another_secret'
    CKEDITOR_HEIGHT = 400
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = 'atelier-heath.light'
    CKEDITOR_FILE_UPLOADER = 'auth.upload'
    UPLOADED_PATH = os.path.join(basedir, 'static/images/')

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL=True
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_USER = "someemail@gmail.com"
    SMTP_PASSWORD = "password"
    SMTP_FROM = "from@flask.com"

class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')