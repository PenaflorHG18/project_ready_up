from typing import Optional
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

class PlayerRegisterForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ", validators=[EqualTo('password')])
    email = EmailField("Email:", validators=[InputRequired()])
    submit = SubmitField("Register")

class EditProfileForm(FlaskForm):
    username = StringField("New Username:")
    email = EmailField("New Email:")
    bio = StringField("Bio:", widget=TextArea())
    submit = SubmitField("Save Changes")


class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    submit = SubmitField("Login")

class GameForm(FlaskForm):
    title = StringField("Title:", validators=[InputRequired()])
    submit = SubmitField("Add to Game List")