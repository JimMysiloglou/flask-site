from .. import db
from flask_login import UserMixin
from . import bcrypt, login_manager
from flask import request
import hashlib


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar_hash = db.Column(db.String(32))
    articles = db.relationship('Article', backref='author', lazy=True)
    projects = db.relationship('Project', backref='author', lazy=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('UTF-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return f"{self.name}: {self.email}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))