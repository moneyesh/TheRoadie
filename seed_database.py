import os
from random import choice,  randint
from datetime import datetime

import crud
import model
import server


os.system("dropdb trips")
os.system('createdb trips')
model.connect_to_db(server.app)
model.db.create_all()

# Create an user
for n in range(5):
    email = f'i.am.user.{n}@tester.com'
    password = 'test'
    fname = f'User{n}'
    lname = f'{n}'

    user = crud.create_user(email, fname, lname, password)
    model.db.session.add(user)

model.db.session.commit()
print(user)


test_trips = [
    {'to_dest': 'Phoenix, Arizona',
     'from_dest': 'Cortez, Colorado',
     'leave_date': '02/05/2023',
     'return_date': '02/13/2023'},

    {'to_dest': 'Phoenix, Arizona',
     'from_dest': 'Rome, Georgia',
     'leave_date': '07/19/2021',
     'return_date': '07/26/2021'},

    {'to_dest': 'Napa, California',
     'from_dest': 'Anderson, South Carolina',
     'leave_date': '04/02/2023',
     'return_date': '04/18/2023'},

    {'to_dest': 'Schaumburg, Illinois',
     'from_dest': 'Atlanta, Georgia',
     'leave_date': '09/04/2023',
     'return_date': '09/08/2023'},

    {'to_dest': 'Dallas, Texas',
     'from_dest': 'Jersey City, New Jersey',
     'leave_date': '07/19/2023',
     'return_date': '07/26/2023'},
]

for item in test_trips:
    leave_date = item['leave_date']
    return_date = item['return_date']
    to_dest = item['to_dest']
    from_dest = item['from_dest']

    user = crud.get_user_by_email('i.am.user.1@tester.com')
    trip = crud.create_trip(leave_date, return_date, to_dest, from_dest, user)
    model.db.session.add(trip)

model.db.session.commit()

#verify that the trip and user is linked
