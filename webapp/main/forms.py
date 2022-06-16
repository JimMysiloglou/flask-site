from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length



class SearchForm(FlaskForm):
    searched = StringField(label="Searched", validators=[DataRequired()])
    submit = SubmitField('Search')


class ContactForm(FlaskForm):
    name = StringField(label='Name *', validators=[DataRequired()])
    email = StringField(label='Email *', validators=[DataRequired(),
                                                Email(granular_message=True)])
    message = TextAreaField(label='Message *', validators=[DataRequired(),
                                                    Length(min=5, max=500)])
    submit = SubmitField(label='Submit')