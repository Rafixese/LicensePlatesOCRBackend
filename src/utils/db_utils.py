# from app import db, User


def delete_user_from_db(user_id: int, User, db):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()


def select_user_from_db(user_id, User):
    return User.query.filter_by(id=user_id).first()


def add_user_to_db(username: str, password: str, User, db):
    db.session.add(User(username=username,
                        password=password))
    db.session.commit()


def get_all_plates(LicensePlate):
    return LicensePlate.query.all()


def delete_plate_from_db(LicensePlate, plate_id, db):
    LicensePlate.query.filter_by(id=plate_id).delete()
    db.session.commit()


def add_license_plate(plate_nb: str, user_id: int, comment: str, db, LicensePlate):
    db.session.add(LicensePlate(plate_nb=plate_nb,
                                user_id=user_id,
                                comment=comment))
    db.session.commit()


def get_all_users(User):
    return User.query.all()


def get_all_plates_for_user(LicensePlate, user_id):
    return LicensePlate.query.filter_by(user_id=user_id).all()
