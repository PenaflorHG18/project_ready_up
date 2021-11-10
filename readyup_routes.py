import os, sys
from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from authentication import Hasher
from readyup_forms import LoginForm, PlayerRegisterForm
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user

# Directory Stuff
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

dbfile = os.path.join(script_dir, "ready_up.sqlite3")
pepfile = os.path.join(script_dir, "pepper.bin")

# open and read the contents of the pepper file into your pepper key
with open(pepfile, 'rb') as fin:
  pepper_key = fin.read()

# create a new instance of Hasher using generated pepper
pwd_hasher = Hasher(pepper_key)

#----------------------#
# App Setup and Config #
#----------------------#
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Prepare and connect the LoginManager to this app
app.login_manager = LoginManager()
app.login_manager.login_view = 'get_login'
@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

#----------------------#
#    Database Setup    #
#----------------------#
# connect database
db = SQLAlchemy(app)

# database model for user
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Unicode, nullable=False)
    username = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary)
    bio = db.Column(db.Unicode, nullable=False)

     # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")
    @password.setter
    def password(self, pwd):
        self.password_hash = pwd_hasher.hash(pwd)
    
    # add a verify_password convenience method
    def verify_password(self, pwd):
        return pwd_hasher.check(pwd, self.password_hash)

# database model for a game
class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)

# add tables to the db (ONLY DO THIS ONCE)
#db.drop_all()
#db.create_all()

#----------------------#
#      App Routes      #
#----------------------#

# registration page routes
@app.get('/register/')
def get_register_form():
    reg_form = PlayerRegisterForm()
    return render_template('registration.j2', form = reg_form)

@app.post('/register/')
def post_register_form():
    reg_form = PlayerRegisterForm()
    if reg_form.validate():
        new_user = User(role="Player", username=reg_form.username.data, password=reg_form.password.data, email=reg_form.email.data)
        db.session.add(new_user)
        db.session.commit()
    else:
        for field,error in reg_form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register_form'))

# login page routes
@app.get('/login/')
def get_login_form():
    log_form = LoginForm()
    return render_template('login.j2', form=log_form)

@app.post('/login/')
def post_login_form():
    log_form = LoginForm()
    if log_form.validate():
        # get user associated with their username
        user = User.query.filter_by(username=log_form.username.data).first()
        if user is not None and user.verify_password(log_form.password.data):
            # log user in
            login_user(user)
            # redirect the user to home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('load_home_page')
            return redirect(next)
        else:
            flash('Invalid username or password')
            return redirect(url_for('get_login_form'))
    else:
        for field, error in log_form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login_form'))

# home page route
@app.get('/home/')
@login_required
def load_home_page():
    pass
