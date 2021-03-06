from typing import Optional
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea
from wtforms.widgets.html5 import ColorInput

class PlayerRegisterForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ", validators=[EqualTo('password')])
    email = EmailField("Email:", validators=[InputRequired()])
    submit = SubmitField("Register")

class AdminRegisterForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ", validators=[EqualTo('password')])
    email = EmailField("Email:", validators=[InputRequired()])
    submit = SubmitField("Register")

class EditProfileForm(FlaskForm):
    color = StringField(widget=ColorInput())
    username = StringField("New Username:")
    email = EmailField("New Email:")
    bio = StringField("Bio:", widget=TextArea())
    icon = SelectField("Icons ", choices=[('cow.svg', 'cow'), ('croc.svg', 'croc'), ('dog.svg', 'dog'), ('dolphin.svg', 'dolphin'), ('fish.svg', 'fish'), ('koala.svg', 'koala'), ('lion.svg', 'lion'), ('panda.svg', 'panda'), ('parrot.svg', 'parrot')])
    submit = SubmitField("Save Changes")

class AdminLogin(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    submit = SubmitField("Login")

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired(), Length(min=8, max=256)])
    submit = SubmitField("Login")

class GameForm(FlaskForm):
    title = StringField("Title:", validators=[InputRequired()])
    submit = SubmitField("Add to Game List")

class MatchmakingForm(FlaskForm):
    title = SelectField("Game:", choices=[])
    submit = SubmitField("Join Matchmaking For This Game")