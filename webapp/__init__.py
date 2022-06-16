from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_assets import Environment, Bundle


db = SQLAlchemy()
migrate = Migrate()
#mail = Mail()

assets_env = Environment()

main_css = Bundle(
    'css/mdb.min.css',
    'css/mdb.min.css.map',
    'css/styles.css',
    output='css/common.css'
)

main_js = Bundle(
    'js/mdb.min.js',
    'js/mdb.min.js.map',
    output='js/common.js'
)


def create_app(object_name):

    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    migrate.init_app(app, db)
    #mail.init_app(app)
    assets_env.init_app(app)

    assets_env.register("main_js", main_js)
    assets_env.register("main_css", main_css)

    from .main import create_module as main_create_module
    from .blog import create_module as blog_create_module
    from .auth import create_module as auth_create_module
    from .portfolio import create_module as portfolio_create_module
    from .admin import create_module as admin_create_module
    
    main_create_module(app)
    blog_create_module(app)
    auth_create_module(app)
    portfolio_create_module(app)
    admin_create_module(app)

    return app