import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Resident, Driver, Drive, Stop
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_drive, create_stop)


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

@user_cli.command("schedule", help="Schedule a Drive to a Street")
@click.argument("driver_id", type=int, default=1)
@click.argument("street", type=str, default="1st Street")
def schedule_drive_command(driver_id, street):
    create_drive(driver_id, street)
    print(f'Drive scheduled for driver number {driver_id} on {street}!')

@user_cli.command("addstop", help="Add a Stop to a Drive")
@click.argument("drive_id", type=int, default=1)
@click.argument("address", type=str, default="123 Main St")
@click.argument("resident_id", type=int, default=1)
def add_stop_command(drive_id, address, resident_id):
    create_stop(drive_id, address, resident_id)
    print(f'Stop added to drive number {drive_id} for resident number {resident_id} at {address}!')

@user_cli.command("viewdriver", help="View status and location of a Driver")
@click.argument("driver_id", type=int, default=1)
def view_driver_command(driver_id):
    driver = db.session.get(Driver, driver_id)
    if driver:
        status = "Available" if driver.status else "Unavailable"
        print(f'Name: {driver.name}, Status: {status}, Location: {driver.location}')
    else:
        print(f'No driver found with ID {driver_id}')

@user_cli.command("viewinbox", help="View Drives scheduled for a Street")
@click.argument("street", type=str, default="1st Street")
def view_inbox_command(street):
    drives = db.session.query(Drive).filter(Drive.street == street).all()
    if drives:
        for drive in drives:
            driver = db.session.get(Driver, drive.driver_id)
            print(f'Drive Number: {drive.id}, Driver Name: {driver.name}, Street: {drive.street}')
    else:
        print(f'No drives scheduled for {street}')

app.cli.add_command(user_cli) # add the group to the cli

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
app.cli.add_command(test)
