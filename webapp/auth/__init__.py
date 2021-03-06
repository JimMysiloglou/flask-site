from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "admin.login_view"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

def create_module(app, **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)