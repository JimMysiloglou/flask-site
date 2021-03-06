from .. import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    subject = db.Column(db.String(64))
    message = db.Column(db.Text(), nullable=False)