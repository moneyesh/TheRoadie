# functions that will populate my model.py
from model import db, User, List, Trip, Task, connect_to_db

# USER FUNCTIONS

def create_user(email, fname, lname, password):
    """Create and returns a new user"""
    user = User(email=email, first_name=fname, last_name=lname, password=password)

    return user


def get_user_by_email(email):
    """ get users with a specific email address"""
    return User.query.filter(User.email == email).first()


def get_user_by_id(id):
    """ get users with a specific email address"""
    return User.query.filter(User.user_id == id).first()




#  TRIP FUNCTIONS 

def create_trip(leave_date, return_date, to_dest, from_dest, user):
    """user creates their trip. Distance should populate from api when destination is chosen. Cost and Budget will be brought in from their functions"""
    trip = Trip(user=user, leave_date=leave_date, return_date=return_date,
                distance=0, to_dest=to_dest, from_dest=from_dest, cost=0, budget=0)

    return trip

def get_trips_by_userid(user_id):

    return Trip.query.filter(Trip.user_id == user_id).all()


# Task and List Functions
def create_task(task, completed):

    task = Task(task=task, completed=completed)

    return task


def create_list(creation_date, list_name):

    list = List(creation_date=creation_date, list_name=list_name)

    return list


