from App.models import User
from App.database import db
from App.models import Resident
from App.models import Driver
from App.models import Drive
from App.models import Stop

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def create_resident(user_id, name, address):
    newresident = Resident(user_id=user_id, name=name, address=address)
    db.session.add(newresident)
    db.session.commit()
    return newresident

def create_driver(user_id, license_number, vehicle_info, location, name,status):
    newdriver = Driver(user_id=user_id, license_number=license_number, vehicle_info=vehicle_info, location=location, name=name,status=status)
    db.session.add(newdriver)
    db.session.commit()
    return newdriver

def create_drive(driver_id, street):
    newdrive = Drive(driver_id=driver_id, street=street)
    db.session.add(newdrive)
    db.session.commit()
    return newdrive

def create_stop(drive_id, address, resident_id):
    newstop = Stop(drive_id=drive_id, address=address, resident_id=resident_id)
    db.session.add(newstop)
    db.session.commit()
    return newstop

def viewInbox(street):
    return db.session.query(Drive).filter(Drive.street == street).all()
     
