from .. import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(50), nullable=False)
    project_description = db.Column(db.String(200), nullable=False)
    project_body = db.Column(db.Text(), nullable=False)
    project_image = db.Column(db.String(30), default='default_project_image.jpg')
    github_link = db.Column(db.String(60))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='project', lazy=True)

    def __repr__(self):
        return f"{self.date_created}: {self.project_title}"