import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Resident, Driver, Drive, Stop
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_drive, create_stop, viewInbox, get_all_drivers, get_all_residents)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 
driver_cli = AppGroup('driver', help='Driver object commands')
resident_cli = AppGroup('resident', help='Resident object commands')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@user_cli.command("list_drivers", help="Lists drivers in the database")
@click.argument("format", default="string")
def list_driver_command(format):
    if format == 'string':
        print(get_all_drivers())
    

@user_cli.command("list_residents", help="Lists residents in the database")
@click.argument("format", default="string")
def list_resident_command(format):
    if format == 'string':
        print(get_all_residents())

@driver_cli.command("schedule", help="Schedule a Drive to a Street")
@click.argument("driver_id", type=int, default=1)
@click.argument("street", type=str, default="123 Main St")
def schedule_drive_command(driver_id, street):
    driver = Driver.query.get(driver_id)
    if driver:
        create_drive(driver_id, street)
    else:
        print(f'No driver found with ID {driver_id}')

@resident_cli.command("addstop", help="Add a Stop to a Drive")
@click.argument("drive_id", type=int, default=1)
@click.argument("house_number", type=int, default=1)
@click.argument("resident_id", type=int, default=1)
def add_stop_command(drive_id, house_number, resident_id):
    
    drive = Drive.query.get(drive_id)
    if drive: 
        address = drive.street
    else:
        print(f'No drive found with ID {drive_id}')
        return
    
    resident = Resident.query.get(resident_id)
    if not resident:
        print(f'No resident found with ID {resident_id}')
        return

    address_1 = resident.address
    address_2 = drive.street
    if address_1 != address_2:
        print(f'Resident address {address_1} does not match drive street {address_2}. Stop not added.')
        return
    
    create_stop(drive_id, house_number, resident_id)
    print(f'Stop added to drive number {drive_id} for resident number {resident_id} at house number {house_number} on {address}!')

@resident_cli.command("viewdriver", help="View status and location of a Driver")
@click.argument("driver_id", type=int, default=1)
def view_driver_command(driver_id):
    driver = db.session.get(Driver, driver_id)
    if driver:
        status = "Available" if driver.status else "Unavailable"
        print(f'Name: {driver.name}, Status: {status}, Location: {driver.location}')
    else:
        print(f'No driver found with ID {driver_id}')

@resident_cli.command("viewinbox", help="View Drives scheduled for a Resident's street")
@click.argument("resident_id", type=int, default=1)
def view_inbox_command(resident_id):
    resident = Resident.query.get(resident_id)
    if not resident:
        print(f'No resident found with ID {resident_id}')
        return
    street = resident.address
    viewInbox(street)
    

app.cli.add_command(user_cli) # add the group to the cli
app.cli.add_command(driver_cli)
app.cli.add_command(resident_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
