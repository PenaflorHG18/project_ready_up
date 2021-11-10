from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy
import os, sys
from sqlalchemy.orm import backref
from readyup_forms import PlayerRegisterForm

# Directory Stuff
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)
dbfile = os.path.join(script_dir, "ready_up.sqlite3")

#----------------------#
# app setup and config #
#----------------------#
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect database
db = SQLAlchemy(app)

# database model for user
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Uniicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)

# database model for game
class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)

# add tables to the db (ONLY DO THIS ONCE)
db.drop_all()
db.create_all()

@app.get('/register/')
def get_register_form():
    reg_form = PlayerRegisterForm()
    return render_template('registration.j2', form = reg_form)

@app.post('/register/')
def post_register_form():
    reg_form = PlayerRegisterForm()
    if reg_form.validate():
        db.session.add(User(username = reg_form.username.data, email = reg_form.email.data))
        db.session.commit()
    else:
        for field,error in reg_form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register_form'))

@app.post('/home/')
def load_home_page():
    pass
