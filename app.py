# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import json
import os

from flask import Flask, Response, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

from src.utils.db_utils import get_all_plates, delete_user_from_db, get_all_users, get_all_plates_for_user, \
    delete_plate_from_db
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
# TODO: ZMIENIĆ !!!!
current_user_id = 1


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
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


@app.route('/license_managment', methods=['POST', 'GET'])
def admin():
    plates = get_all_plates_for_user(LicensePlate, current_user_id)
    return render_template('admin.html', page_title="Admin Panel", plates=plates)


@app.route('/delete_user/<plate_id>', methods=["POST", "GET"])
def delete_plate(plate_id):
    delete_plate_from_db(LicensePlate, plate_id, db)
    return render_template("delete_plate.html")


# main driver function


if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
