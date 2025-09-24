from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    #relationships
    residents = db.relationship('Resident', backref='user', lazy=True)
    drivers = db.relationship('Driver', backref='user', lazy=True)
    

class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def create_stop(self, drive_id, house_number):
        newstop = Stop(drive_id=drive_id, house_number=house_number, resident_id=self.id)
        db.session.add(newstop)
        db.session.commit()
        return newstop
    
    #relationships
    stops = db.relationship('Stop', backref='resident', lazy=True)
    

    
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    license_number = db.Column(db.String(20), nullable=False)
    vehicle_info = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(50), nullable=False)

    def create_drive(self, street):
        
        streets = Resident.query.with_entities(Resident.address).all()
        for s in streets:
            if street == s[0]:
                newdrive = Drive(driver_id=self.id, street=street)
                db.session.add(newdrive)
                db.session.commit()
                print(f'Drive scheduled for driver number {self.id} on {street}!')
                return newdrive
            else: 
                print(f'Street {street} not found in resident addresses.')
                return None
        
        
    
    #relationships
    drives = db.relationship('Drive', backref='driver', lazy=True)
    
   
    
class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    
    #relationships
    stops = db.relationship('Stop', backref='drive', lazy=True)
    
    
class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    
    


