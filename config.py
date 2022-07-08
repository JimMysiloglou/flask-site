import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'another_secret'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    CKEDITOR_HEIGHT = 400
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = 'atelier-heath.light'
    CKEDITOR_FILE_UPLOADER = 'auth.upload'
    UPLOADED_PATH = os.path.join(basedir, 'static/images/')
    SSL_REDIRECT = False



class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=os.environ.get("db_username"),
    password=os.environ.get("db_password"),
    hostname=os.environ.get("db_hostname"),
    databasename=os.environ.get("db_name"),
    )

    SQLALCHEMY_POOL_RECYCLE = 299
    SSL_REDIRECT = bool(os.environ.get('PYTHONANYWHERE_DOMAIN'))

        


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')