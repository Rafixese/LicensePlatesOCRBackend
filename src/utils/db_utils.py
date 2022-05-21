from database_init import db, User, LicensePlate


def delete_user_from_db(user_id: int):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()


def select_user_from_db(user_id):
    return User.query.filter_by(id=user_id).first()


def add_user_to_db(user_id: int, username: str, password: str):
    db.session.add(User(id=user_id,
                        username=username,
                        password=password))
    db.session.commit()


def get_all_plates():
    return LicensePlate.query.all()


def add_license_plate(id: int, plate_nb: str, user_id: int, comment: str):
    db.session.add(LicensePlate(id=id,
                                plate_nb=plate_nb,
                                user_id=user_id,
                                comment=comment))
    db.session.commit()
