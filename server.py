from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud
import json
from jinja2 import StrictUndefined
import os
import requests
from datetime import date

app = Flask(__name__)

app.secret_key = "devok"
app.jinja_env.undefined = StrictUndefined

FRONT_GOOGLE = os.environ['FRONT_GOOGLE']
BACK_GOOGLE = os.environ['BACK_GOOGLE']
MY_WEATHER = os.environ['MY_WEATHER']
HOTEL_GOOGLE = os.environ['HOTEL_GOOGLE']

# REGISTRATION AND LOGIN
@app.route("/")
def homepage():

    return render_template('homepage.html')


@app.route("/register", methods=["POST"])
#user registration section
def register_user():
    # For creating a new user
    fname = request.form.get("first name")
    lname = request.form.get("last name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_pw = request.form.get("confirm password")
    user = crud.get_user_by_email(email)
    # print(user)
    if user:
        flash("This email alreadys exists. Please log in.")
    else:
        if password == confirm_pw:
            user = crud.create_user(email, fname, lname, password)
            # can this go in crud as a part of the function or does it need to be here
            db.session.add(user)
            db.session.commit()
            flash("Account created successfuly! Please log in.")
        else:
            flash("The passwords do not match. Please try again.")

    return redirect('/')


@app.route("/login", methods=["POST"])
#user login section
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        print('invalid user')
        return redirect("/homepage")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email

        return redirect('/dashboard')


@app.route("/dashboard")
#user dashboard
def dashboard():
    # checks the users logged in email and displays the dashboard with their info.
    logged_in_email = session.get("user_email")
    if logged_in_email is None:
        return redirect("/")
    user = crud.get_user_by_email(logged_in_email)
    trips = crud.get_trips_by_userid(user.user_id)
    soonest_trip = ""
    countdown = None 
    for trip in trips:        
        if trip.leave_date > date.today():
            trip_countdown = trip.leave_date - date.today() #creates a time delta object (days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
            print(trip_countdown)
            if countdown is None or trip_countdown < countdown:
                countdown = trip_countdown
            soonest_trip = trip.to_dest
    # print(soonest_trip)
    # print(countdown)
    return render_template("user_dashboard.html", trips=trips, user=user, soonest_trip=soonest_trip, countdown=countdown)


@app.route("/logout")
def user_logout():
    session.pop("user_id", None)
    flash("You have successfully logged out")
    return redirect("/")

#MAP
@app.route("/map")
def map():
    # displays the map page
    return render_template("map.html", FRONT_GOOGLE=FRONT_GOOGLE)


@app.route("/map/waypoints")
def get_waypoints():
    from_dest = request.args.get('from')
    # print('***from',from_dest)
    to_dest = request.args.get('to')
    # print('***to', to_dest)
    google_response = requests.get(
        f"https://maps.googleapis.com/maps/api/directions/json?destination={to_dest}&origin={from_dest}&key={BACK_GOOGLE}").json()
    # weather_response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={MY_WEATHER}&q=Atlanta&aqi=no').json()
    # print('*******', google_response)
    leg = google_response['routes'][0]['legs'][0]
    waypoints = [leg['start_location']]
    # print(waypoints)
    distance = [leg['distance']]
    print('!!!DIST!!!!',distance)
   
    for step in leg['steps']:
        waypoints.append(step['end_location'])
    return jsonify(waypoints, distance)


@app.route("/waypoint-weather")
def way_weather():
    q = request.args.get("q")
   
    weather_response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={MY_WEATHER}&q={q}&aqi=no').json()
    # print(weather_response)
    forecast_text = weather_response.get('current').get('condition').get('text')
    forecast_icon = weather_response.get('current').get('condition').get('icon')    
    forecast = {"forecast_icon": forecast_icon, "forecast_text": forecast_text}
    return jsonify(forecast)


# TRIPS
@app.route("/my-trips")
def my_trips():
 # this will populate the trips on the past trips page.
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    trips = crud.get_trips_by_userid(user.user_id)

    past_trip_list = []
    future_trip_list = []
    today = date.today()
    
    for trip in trips:
        if trip.return_date < today:
            # print(trip)
            past_trip_list.append(trip)
            # print(past_trip_list)
        elif trip.leave_date > today:
            future_trip_list.append(trip)    
        
    return render_template("my-trips.html", trips=trips, future_trip_list=future_trip_list, past_trip_list=past_trip_list)


@app.route("/my-trips/create-trip", methods=["POST"])
# Create new trips
def create_my_trips():
    leave_date = request.json.get('depart_date')
    return_date = request.json.get('return_date')
    # print(leave_date,return_date)
    to_dest = request.json.get('to')
    from_dest = request.json.get('from')
    to_do = request.json.get('to_do_list_items')
    list_name = request.json.get('list_name')
    # print(to_do)
    logged_in_email = session.get('user_email')
    user = crud.get_user_by_email(logged_in_email)

    create_trip = crud.create_trip(leave_date, return_date, to_dest, from_dest, user)
    db.session.add(create_trip)
    create_list = crud.create_list(create_trip, date.today(), list_name)
    db.session.add(create_list)
    for to_do_item in to_do:
        create_to_do = crud.create_to_do(create_list, to_do_item)
        db.session.add(create_to_do)
    db.session.commit()
    flash("Trip created successfully!") 
    return jsonify("Trip created successfully!")


@app.route("/update", methods=['POST'])
#update trip page
def update():
    upcoming_trip = request.form.get("future_trip")
    trip = crud.get_trips_by_tripid(upcoming_trip)
    # trip_id = trip.trip_id
    
    return render_template('update-trip.html', trip=trip)

@app.route("/update/<trip_id>", methods=['POST'])
# this route is for updating the trip details on the update page
def update_trip(trip_id):
    trip = crud.get_trips_by_tripid(trip_id)
    to_dest_to_update = request.form.get("to")
    from_dest_to_update = request.form.get("from")
    leave_date_to_update = request.form.get("depart_date")
    return_date_to_update = request.form.get("return_date")
    trip.to_dest = to_dest_to_update
    trip.from_dest = from_dest_to_update
    trip.leave_date = leave_date_to_update
    trip.return_date = return_date_to_update

    db.session.commit()
    flash("Your trip has been updated successfully!") 
    return redirect('/my-trips')

@app.route("/update/to-do", methods=['POST'])
#update an exisisting to-do from trip
def update_to_do():

    id = request.json["task_id"]
    name = request.json["task"]
    to_do = crud.find_to_do_by_id(id)
    # print(to_do)
    to_do.to_do = name
    db.session.commit()
    return "Success"

@app.route("/remove/to-do", methods=['POST'])
#remove an exisisting to-do from trip
def remove_to_do():

    id = request.json["task_id"]
    to_do = crud.find_to_do_by_id(id)
    print(to_do)
    db.session.delete(to_do)
    db.session.commit()
    return "Item Removed"

@app.route("/add/new-to-do", methods=["POST"])
#add a to-do to existing trip
def add_new_to_do():
    id = request.json["list_id"]
    print(id)
    item_added = request.json.get('new_updated_to_do_item')
    # new_to_do_created = crud.create_to_do(item_added)
    existing_list = crud.get_list_by_id(id)
    print('***List:' , existing_list)
    print('***Item:',item_added)
    create_to_do = crud.create_to_do(existing_list, item_added)
    db.session.add(create_to_do)
    db.session.commit()
    return jsonify({'task_id': create_to_do.task_id, 'to_do': create_to_do.to_do})


# gas calculator
@app.route("/gas-calc")
def gas():

    return render_template("gas-calc.html")

@app.route("/hotels")
def hotels():
    return render_template("hotels.html", HOTEL_GOOGLE=HOTEL_GOOGLE)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=5001)
