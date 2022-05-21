import json
import os

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

from src.utils.db_utils import get_all_plates, delete_license_plate_from_db, insert_license_plate_to_db
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


@app.route('/')
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


@app.route('/insert_license_plate')
def insert_license_plate():
    plate_nb = request.args.get('plate_nb')
    plate_comment = request.args.get('plate_comment')
    # TODO USERA DODAC :~D!!!
    user_id = 1

    # Plate duplicate
    if LicensePlate.query.filter_by(plate_nb=plate_nb).first():
        return Response(status=404)

    insert_license_plate_to_db(plate_nb=plate_nb, user_id=user_id, comment=plate_comment, db=db,
                               LicensePlate=LicensePlate)
    return Response(status=200)


@app.route('/delete_license_plate')
def delete_license_plate():
    plate_nb = request.args.get('plate_nb')

    # There are no plate with plate_nb number
    if not LicensePlate.query.filter_by(plate_nb=plate_nb).first():
        return Response(status=404)

    delete_license_plate_from_db(plate_nb=plate_nb, db=db, LicensePlate=LicensePlate)
    return Response(status=200)


if __name__ == '__main__':
    app.run()
