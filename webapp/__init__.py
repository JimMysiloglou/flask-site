from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()




def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    migrate.init_app(app, db)
    

    from .main import create_module as main_create_module
    from .blog import create_module as blog_create_module
    from .auth import create_module as auth_create_module
    from .portfolio import create_module as portfolio_create_module
    from .admin import create_module as admin_create_module
    from .babel import create_module as babel_create_module
    
    main_create_module(app)
    blog_create_module(app)
    auth_create_module(app)
    portfolio_create_module(app)
    admin_create_module(app)
    babel_create_module(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

    

    return app