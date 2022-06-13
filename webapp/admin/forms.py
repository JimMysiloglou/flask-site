from wtforms import (
    widgets,
    TextAreaField,
    PasswordField,
    BooleanField,
    StringField,
    SubmitField
)
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_wtf.file import FileField, FileAllowed


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


class AccountUpdateForm(FlaskForm):
    name = StringField(label="Name",
                       validators=[DataRequired(message="This field should not be blank"),
                                   Length(min=3, max=30, message="This field should be 3 to 30 characters long")])

    email = EmailField(label="Email",
                       validators=[DataRequired(message="This field cannot be blank"),
                                   Email(message="Please fill a proper email")])

    password = PasswordField(label="Password",
                             validators=[DataRequired(message="This field cannot be blank"),
                             Length(min=4, max=16, message="The password should be 4 to 16 characters long")])

    password2 = PasswordField(label="Password validation",
                              validators=[DataRequired(message="This field cannot be blank"),
                                          Length(min=4, max=16, message="This password should be 4 to 16 characters long"),
                                          EqualTo("password", message="This password should be the same with the above")])

    profile_image = FileField("Profile image",
                              validators=[Optional(strip_whitespace=True),
                                          FileAllowed(['jpg', 'jpeg', 'png'],
                                          message="Only jpg, jpeg and png files allowed")])

    submit = SubmitField("Submit")