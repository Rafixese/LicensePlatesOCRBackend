import json
import os

from flask import Flask, Response, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask import Flask, Response, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from src.utils.db_utils import get_all_plates, delete_license_plate_from_db, insert_license_plate_to_db, \
    get_all_plates_for_user
from src.utils.license_plates_comparator import LicensePlatesComparator
from src.utils.solutionutils import get_project_root

app = Flask(__name__, template_folder='./src/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(get_project_root(), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'qwerty'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
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


@app.route('/')
def index():
    return render_template('home.html', title='Home')


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))
    login_user(user, remember=remember)
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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


@app.route('/license_management', methods=['POST', 'GET'])
def license_management():
    plates = get_all_plates_for_user(LicensePlate=LicensePlate, user_id=current_user_id)
    if request.method == 'POST':
        return redirect(url_for("add_plate"))
    return render_template('license_management.html', page_title="Admin Panel", plates=plates)


@app.route('/delete_license_plate/<plate_nb>', methods=["POST", "GET"])
def delete_plate(plate_nb):
    # There are no plate with plate_nb number
    if request.method == 'POST':
        return redirect(url_for("license_management"))
    if not LicensePlate.query.filter_by(plate_nb=plate_nb).first():
        return Response(status=404)

    delete_license_plate_from_db(plate_nb=plate_nb, db=db, LicensePlate=LicensePlate)

    return render_template("delete_plate.html")


@app.route('/add_plate', methods=["POST", "GET"])
def add_plate():
    if request.method == 'POST':
        plate_nb = request.form['plate_nb']
        comment = request.form['comment']

        insert_license_plate_to_db(plate_nb=plate_nb, user_id=current_user_id, comment=comment, db=db,
                                   LicensePlate=LicensePlate)
        return redirect(url_for("license_management"))
    return render_template("add_plate.html")


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


# @app.route('/delete_license_plate')
# def delete_license_plate():
#     plate_nb = request.args.get('plate_nb')
#
#     # There are no plate with plate_nb number
#     if not LicensePlate.query.filter_by(plate_nb=plate_nb).first():
#         return Response(status=404)
#
#     delete_license_plate_from_db(plate_nb=plate_nb, db=db, LicensePlate=LicensePlate)
#     return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True)
