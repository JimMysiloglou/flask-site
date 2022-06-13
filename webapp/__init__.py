from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
#migrate = Migrate()
#mail = Mail()

def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    #migrate.init_app(app, db)
    #mail.init_app(app)

    from .main import create_module as main_create_module
    from .blog import create_module as blog_create_module
    from .auth import create_module as auth_create_module
    from .admin import create_module as admin_create_module
    
    main_create_module(app)
    blog_create_module(app)
    auth_create_module(app)
    admin_create_module(app)

    return app