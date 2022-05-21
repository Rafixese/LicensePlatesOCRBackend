from database_init import db, User, LicensePlate


def delete_user_from_db(user_id: int):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()


def select_user_from_db(user_id):
    return User.query.filter_by(id=user_id).first()


def add_user_to_db( username: str, password: str):
    db.session.add(User(username=username,
                        password=password))
    db.session.commit()


def get_all_plates():
    return LicensePlate.query.all()


def add_license_plate( plate_nb: str, user_id: int, comment: str):
    db.session.add(LicensePlate(plate_nb=plate_nb,
                                user_id=user_id,
                                comment=comment))
    db.session.commit()

add_user_to_db("Pawel5","DUPA")
add_user_to_db("Pawel2","DUPA")
add_user_to_db("Pawel3","DUPA")
add_user_to_db("Pawe4l","DUPA")
add_license_plate("KKKKKK",1,"")
add_license_plate("KKKKK2",1,"")
add_license_plate("KKKKK3",1,"")
add_license_plate("KKKKK4",1,"")
add_license_plate("KKKKK5",1,"")
add_license_plate("KKKKK6",1,"")