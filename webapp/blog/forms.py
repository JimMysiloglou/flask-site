from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class CommentForm(FlaskForm):
    author = StringField(label="Name *",
                         validators=[DataRequired(message="This field cannot be blank"),
                         Length(min=3, max=30, message="This field should be 3 to 30 characters long")])

    email = EmailField(label="Email *",
                       validators=[Email(message="Please fill a proper email")])

    text = TextAreaField(label="Comment *",
                         validators=[DataRequired(message="This field should not be blank"),
                                     Length(min=3, max=300, message="This field should be 3 to 300 characters long")])

    submit = SubmitField("Submit")
