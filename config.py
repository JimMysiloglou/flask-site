import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    WTF_CSRF_SECRET_KEY = 'another_secret'
    RECAPTCHA_PUBLIC_KEY = '6Lee0YYgAAAAAAjAxq3Op4uI_WHMLLSvjzaet-QO'
    RECAPTCHA_PRIVATE_KEY = '6Lee0YYgAAAAAIRg0TOyBxXr6JpMJ-MDn6fk2VGK'
    CKEDITOR_HEIGHT = 400
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = 'atelier-heath.light'
    CKEDITOR_FILE_UPLOADER = 'auth.upload'
    UPLOADED_PATH = os.path.join(basedir, 'static/images/')

class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class DevConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')