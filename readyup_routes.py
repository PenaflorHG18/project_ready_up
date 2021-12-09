# Imports
import os, sys
import datetime
from flask import Flask, request, render_template, redirect, url_for, abort, jsonify
from flask import flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.orm.query import Query
from authentication import Hasher
from readyup_forms import AdminRegisterForm, EditProfileForm, GameForm, LoginForm, MatchmakingForm, PlayerRegisterForm
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

# Connect LoginManager to app
app.login_manager = LoginManager()
app.login_manager.login_view = 'get_login'
@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

#----------------------#
#    Database Setup    #
#----------------------#

## connect database ##

db = SQLAlchemy(app)

## database model for user ##

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, nullable=False)
    username = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary)
    bio = db.Column(db.Unicode, nullable=True)
    email = db.Column(db.Unicode, nullable=False)
    last_active = db.Column(db.DateTime, nullable=True)
    curr_game = db.Column(db.Integer, db.ForeignKey('Games.id'), nullable=True)
    icon = db.Column(db.Unicode, nullable=False)
    icon_color = db.Column(db.Unicode, nullable=True)

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

## database model for a game ##

class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode, nullable=False)
    status = db.Column(db.Unicode, nullable=False)
    users = db.relationship('User', backref='game')

## add tables to the db (ONLY DO THIS ONCE) ##
# db.drop_all()
# db.create_all()
# admin_one = User(role=0, username='PlayerOne', password='readyup2021#', email='PlayerOne@gmail.com', icon='/static/images/fish.svg')
# player_one = User(role=1, username='Harry', password='password1', email='harry@gmail.com', icon='/static/images/panda.svg')
# game_one = Game(title='Destiny', status='approved')
# db.session.add(player_one)
# db.session.add(admin_one)
# db.session.add(game_one)
# db.session.commit()

#----------------------#
#      App Routes      #
#----------------------#

## api routes ##
@app.delete('/reviewgames/<int:game_id>')
def remove_game(game_id):
    game = Game.query.filter_by(id=game_id).first()
    db.session.delete(game)
    db.session.commit()
    return 'Success'

@app.post('/reviewgames/<int:game_id>')
def approve_game(game_id):
    game = Game.query.filter_by(id=game_id).first()
    game.status = 'approved'
    db.session.add(game)
    db.session.commit()
    return 'Success'

@app.delete('/reviewplayer/<int:user_id>')
def remove_player(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return 'Success'

## player registration page routes ##
@app.get('/register/')
def get_register_form():
    # TODO: Make this look nicer using bootstrap
    reg_form = PlayerRegisterForm()
    return render_template('registration.j2', form = reg_form)

@app.post('/register/')
def post_register_form():
    reg_form = PlayerRegisterForm()
    if reg_form.validate():
        user = User.query.filter_by(username=reg_form.username.data).first()
        if user is None:
            new_user = User(role=1, username=reg_form.username.data, password=reg_form.password.data, email=reg_form.email.data, icon='/static/images/fish.svg')
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('get_login_form'))
        else:
            flash("Username Taken!")
            return redirect(url_for('get_register_form'))
    else:
        for field,error in reg_form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register_form'))

## admin registration page routes ##

@app.get('/register/admin/')
def get_register_admin():
    # TODO: Make this look nicer using bootstrap
    reg_form = AdminRegisterForm()
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return render_template('admin_registration.j2', form = reg_form, user = user)

@app.post('/register/admin/')
def post_register_admin():
    reg_form = AdminRegisterForm()
    if reg_form.validate():
        new_user = User(role=0, username=reg_form.username.data, password=reg_form.password.data, email=reg_form.email.data, icon='/static/images/fish.svg')
        db.session.add(new_user)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('get_register_admin'))
    else:
        for field,error in reg_form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register_admin'))

## Game Review ##

@app.route('/reviewgames/')
@login_required
def review_games():
    role = session.get('curr_role')
    game_list = Game.query.filter_by(status='unapproved').all()
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return render_template('review_games.j2', role = role, games = game_list, user = user)

## Player Review ##

@app.route('/reviewplayers/')
@login_required
def review_players():
    role = session.get('curr_role')
    player_list = User.query.filter_by(role=1).all()
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return render_template('review_players.j2', role = role, players = player_list, user = user)

## profile page routes ##

@app.route('/profile/')
@login_required
def view_profile():
    # TODO: get the current user and display their information to the screen
    edit = False
    role = session.get('curr_role')
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return render_template('profile_page.j2', user = user, edit = edit, role = role)

@app.get('/profile/edit/')
@login_required
def edit_profile():
    # TODO: create profile icon creation palatte in 'edit_profile.j2' using JS and AJAX
    edit = True
    role = session.get('curr_role')
    form = EditProfileForm()
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return render_template('profile_page.j2', form = form, user = user, edit = edit, role = role)

@app.post('/profile/edit/')
def post_edit_form():
    form = EditProfileForm()
    user = User.query.filter_by(username=session.get('curr_user')).first()
    if form.validate():
        if form.username.data != '':
            user.username = form.username.data
            session['curr_user'] = form.username.data
        if form.email.data != '':
            user.email = form.email.data
        if form.bio.data != '':
            user.bio = form.bio.data
        if form.color.data != '':
            user.icon_color = form.color.data
        user.icon = "/static/images/" + form.icon.data
        db.session.add(user)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('edit_profile'))
    else:
        for field,error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('edit_profile'))

## Adding Game Route ##

@app.get('/addgame/')
def get_game_form():
    # TODO: Make this look nicer using bootstrap
    add_form = GameForm()
    role = session.get('curr_role')
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return render_template('add_game_page.j2', form = add_form, role = role, user = user)

@app.post('/addgame/')
def post_game_form():
    add_form = GameForm()
    if add_form.validate():
        new_game = Game(title=add_form.title.data, status='unapproved')
        db.session.add(new_game)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('get_game_form'))
    else:
        for field,error in add_form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_game_form'))

## login page routes ##

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
            session['curr_user'] = log_form.username.data
            session['curr_role'] = user.role
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

## logout ##

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('load_home_page'))

## Matchmaking Routes ##

@app.route('/matchmaking/')
@login_required
def load_matchmaking():
    role = session.get('curr_role')
    game_list = Game.query.filter_by(status='approved').all()
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return render_template('matchmaking_page.j2', role = role, games = game_list, user = user)

@app.route('/queue/<int:id>')
@login_required
def load_queue(id):
    game = Game.query.filter_by(id=id).first()
    user = User.query.filter_by(username=session.get('curr_user')).first()
    role = session.get('curr_role')
    user.curr_game = id
    user.last_active = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    players = User.query.filter_by(curr_game=id).all()
    final = []
    for player in players:
        time_diff = user.last_active - player.last_active
        minutes = abs(time_diff.seconds / 60)
        if minutes <= 15:
            final.append(player)
    return render_template('queue.j2', players = final, game = game, user = user, role = role)

## home page route ##

@app.get('/home/')
def load_home_page():
    logged_in = current_user
    user_role = session.get('curr_role')
    user = User.query.filter_by(username=session.get('curr_user')).first()
    game_list = Game.query.filter_by(status='approved').all()
    return render_template('home_page.j2', logged_in = logged_in.is_authenticated, role = user_role, user = user, games = game_list)

@app.route('/')
def index():
    user = User.query.filter_by(username=session.get('curr_user')).first()
    return redirect(url_for('load_home_page'))
