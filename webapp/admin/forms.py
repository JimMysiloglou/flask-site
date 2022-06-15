from wtforms import (
    widgets,
    TextAreaField,
    PasswordField,
    BooleanField
)
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class LoginForm(FlaskForm):
    email = EmailField(label="Email",
                       validators=[DataRequired(message="This field cannot be blank"),
                                   Email(message="Please fill a proper email address")])

    password = PasswordField(label="Password",
                             validators=[DataRequired(message="This field cannot be blank")])

    remember_me = BooleanField(label="Remember me")