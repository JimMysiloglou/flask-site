from .models import db

def create_module(app, **kwargs):
    from .controllers import portfolio_blueprint
    app.register_blueprint(portfolio_blueprint)