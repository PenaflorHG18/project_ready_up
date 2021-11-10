from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, Email, Optional

class PlayerRegisterForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    email = EmailField("Email:", validators=[InputRequired()])
    submit = SubmitField("Register")

class GameForm(FlaskForm):
    title = StringField("Title:", validators=[InputRequired()])
    submit = SubmitField("Add to Game List")