from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields.html5 import EmailField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_babel import lazy_gettext as _l


class CommentForm(FlaskForm):
    author = StringField(label=_l("Name *"),
                         validators=[DataRequired(),
                         Length(min=3, max=30)])

    email = EmailField(label=_l("Email *"),
                       validators=[DataRequired(), Email()])

    text = TextAreaField(label=_l("Comment *"),
                         validators=[DataRequired(),
                                     Length(min=3, max=300)])

    recaptcha = RecaptchaField()

    submit = SubmitField(_l("Submit"))
