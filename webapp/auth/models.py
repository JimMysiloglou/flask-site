from .. import db
from flask_login import UserMixin
from . import bcrypt, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(32), default='default_profile_image.jpg')
    articles = db.relationship('Article', backref='author', lazy=True)
    #projects = db.relationship('Project', backref='author', lazy=True)
    
    def __repr__(self):
        return f"{self.name}: {self.email}"

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))