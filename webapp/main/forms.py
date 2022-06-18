from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_babel import lazy_gettext as _l



class SearchForm(FlaskForm):
    searched = StringField(label=_l("Searched"), validators=[DataRequired()])
    submit = SubmitField('Search')


class ContactForm(FlaskForm):
    name = StringField(label=_l('Name *'), validators=[DataRequired()])
    email = StringField(label=_l('Email *'), validators=[DataRequired(),
                                                Email(granular_message=True)])
    message = TextAreaField(label=_l('Message *'), validators=[DataRequired(),
                                                    Length(min=5, max=500)])
    submit = SubmitField(label=_l('Submit'))