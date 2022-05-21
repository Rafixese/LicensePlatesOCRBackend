# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import json
import os

from flask import Flask, Response, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from src.utils.db_utils import get_all_plates
from src.utils.license_plates_comparator import LicensePlatesComparator
from src.utils.solutionutils import get_project_root

app = Flask(__name__, template_folder='./src/templates')
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


@app.route('/')
def index():
    return render_template('home.html', title='Home')


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/register')
def register():
    return render_template('register.html', title='Register')


@app.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    password = request.form.get('password')
    try:
        new_user = User(username=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        return Response(status=400)
    return redirect(url_for('login'))


@app.route('/check_license/<plate_nb>')
def get_info_about_plate(plate_nb: str):
    plates = get_all_plates(LicensePlate)
    comparator = LicensePlatesComparator()

    for plate in plates:
        if comparator.compare_license_plates_strings(plate_nb, plate.plate_nb):
            return Response(json.dumps({'plate': plate.plate_nb, 'comment': plate.comment}), status=200,
                            mimetype='application/json')

    return Response(status=404)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
