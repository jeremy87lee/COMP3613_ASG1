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
    driver = Driver.query.get(driver_id)
    driver.create_drive(street)
    

def create_stop(drive_id, house_number, resident_id):
    resident = Resident.query.get(resident_id)
    resident.create_stop(drive_id, house_number)
    
    
    

def viewInbox(street):
    drives = db.session.query(Drive).filter(Drive.street == street).all()
    if drives:
        for drive in drives:
            print(f'Drive ID: {drive.id}, Driver ID: {drive.driver_id}, Street: {drive.street}')
            
    else: 
        print(f'No drives scheduled for {street}, which is the resident\'s street')

def get_all_drivers():
    drivers = db.session.scalars(db.select(Driver)).all()
    if not drivers:
        print('No drivers found.')
        return []
    for driver in drivers:
        print(f'Driver ID: {driver.id}, Name: {driver.name}, Vehicle Info: {driver.vehicle_info}, Location: {driver.location}')
        if driver.status:
            print(f', Status: Available')
        else:
            print(f', Status: Not available')
    return drivers

def get_all_residents():
    residents = db.session.scalars(db.select(Resident)).all()
    if not residents:
        print('No residents found.')
        return []
    for resident in residents:
        print(f'Resident ID: {resident.id}, Name: {resident.name}, Address: {resident.address}')
    return residents

def get_all_drives():
    drives = db.session.scalars(db.select(Drive)).all()
    if not drives:
        print('No drives found.')
        return []
    for drive in drives:
        print(f'Drive ID: {drive.id}, Driver ID: {drive.driver_id}, Street: {drive.street}')
    return drives

def get_all_stops():
    stops = db.session.scalars(db.select(Stop)).all()
    if not stops:
        print('No stops found.')
        return []
    for stop in stops:
        print(f'Stop ID: {stop.id}, Drive ID: {stop.drive_id}, House Number: {stop.house_number}, Resident ID: {stop.resident_id}')
    return stops