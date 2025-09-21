from .user import create_user,create_driver,create_resident,create_drive,create_stop
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_user('alice', 'alicepass')
    create_user('rob', 'robpass')
    create_user('jane', 'janepass')
    create_user('tom', 'tompass')
    create_user('lisa', 'lisapass')
    create_resident(1, 'Bob', '123 Main St')
    create_resident(2, 'Alice', '456 Oak Ave')
    create_driver(3, 'D1234567', 'Toyota Camry', 'Downtown', 'Rob', False)
    create_driver(4, 'D7654321', 'Honda Accord', 'Uptown', 'Jane', True)
    create_resident(5, 'Tom', '789 Pine Rd')
    create_driver(6, 'D1122334', 'Ford Focus', 'Midtown', 'Lisa', True)
