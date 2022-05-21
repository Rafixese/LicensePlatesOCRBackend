def delete_user_from_db(user_id: int, User, db):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()


def select_user_from_db(user_id, User):
    return User.query.filter_by(id=user_id).first()


def insert_user_to_db(username: str, password: str, User, db):
    db.session.add(User(username=username,
                        password=password))
    db.session.commit()


def get_all_plates(LicensePlate):
    return LicensePlate.query.all()


def insert_license_plate_to_db(plate_nb: str, user_id: int, comment: str, db, LicensePlate):
    db.session.add(LicensePlate(plate_nb=plate_nb,
                                user_id=user_id,
                                comment=comment))
    db.session.commit()


def delete_license_plate_from_db(plate_nb: str, db, LicensePlate):
    LicensePlate.query.filter_by(plate_nb=plate_nb).delete()
    db.session.commit()
