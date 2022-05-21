# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import json
import os

from flask import Flask, Response, Blueprint, render_template, redirect, url_for, request
from flask_login import UserMixin, LoginManager, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from src.utils.db_utils import get_all_plates
from src.utils.license_plates_comparator import LicensePlatesComparator
from src.utils.solutionutils import get_project_root


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(get_project_root(), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class LicensePlate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plate_nb = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Plate %r>' % self.plate_nb


db.create_all()
db.session.commit()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
# @login_required
def hello_world():
    return 'Hello World'


@app.route('/check_license/<plate_nb>')
def get_info_about_plate(plate_nb: str):
    plates = get_all_plates(LicensePlate)
    comparator = LicensePlatesComparator()

    for plate in plates:
        if comparator.compare_license_plates_strings(plate_nb, plate.plate_nb):
            return Response(json.dumps({'plate': plate.plate_nb, 'comment': plate.comment}), status=200,
                            mimetype='application/json')

    return Response(status=404)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login_reg.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('/login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('/home'))

@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redir`ect back to signup page so user can try again
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('/login'))

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
