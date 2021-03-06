from flask import request
from .. import db
from datetime import datetime
import hashlib
import re

PATTERN = "(?<=id=[\u0027\u0022])[a-zA-z]+(?=[\u0027\u0022])"


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.String(2), nullable=False)
    article_title = db.Column(db.String(50), nullable=False)
    article_description = db.Column(db.String(200), nullable=False)
    article_body = db.Column(db.Text(), nullable=False)
    article_image = db.Column(db.String(30), default='default_article_image.jpg')
    article_section_ids = db.Column(db.String(60))
    article_sections = db.Column(db.String(300))
    github_link = db.Column(db.String(60))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                backref=db.backref('articles', lazy='dynamic'))
    comments = db.relationship('Comment', backref='article', lazy=True)

    def __init__(self, **kwargs):
        super(Article, self).__init__(**kwargs)
        if self.article_section_ids is None:
            self.article_section_ids = self.section_scraping()

    def section_scraping(self):
        return '|'.join(re.findall(PATTERN, self.article_body))

    @property
    def sections(self):
        ids = self.article_section_ids or self.section_scraping()
        return dict(zip(ids.split('|'), self.article_sections.split('|')))

    def __repr__(self):
        return f"{self.date_created}: {self.article_title}"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))

    def __repr__(self):
        return f"{self.name}: {self.description}"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    email= db.Column(db.String(150), nullable=False)
    avatar_hash = db.Column(db.String(32))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

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
        return f"{self.author}: {self.text}"