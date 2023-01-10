# functions that will populate my model.py
from model import db, User, List, Trip, ToDo, connect_to_db

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

def get_trips_by_tripid(trip_id):

    return Trip.query.get(trip_id) 

#update trip details
def update_trip(trip_id):
    
                
    return Trip.query.get(trip_id)


# Task and List Functions
def create_to_do(list, to_do, completed=False):

    to_dos = ToDo(list=list, to_do=to_do, completed=completed)

    return to_dos


def create_list(trip, creation_date, list_name):

    list = List(trip=trip, creation_date=creation_date, list_name=list_name)

    return list

def find_to_do_by_id(id):

    return ToDo.query.get(id)

def get_list_by_id(id):

    return List.query.get(id)

def check_checkbox(id):

    return ToDo.query.get(id)

