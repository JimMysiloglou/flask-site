import os
from webapp import create_app, db
from webapp.blog.models import Article, Comment, Tag
from webapp.auth.models import User
from webapp.auth import bcrypt

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app(f'config.{env.capitalize()}Config')

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, bcrypt=bcrypt, User=User, Article=Article, Tag=Tag)


if __name__ == '__main__':
    app.run()