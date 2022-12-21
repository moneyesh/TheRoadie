from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, db
import crud
import json
from jinja2 import StrictUndefined
import os
import requests
from datetime import date, datetime

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

FRONT_GOOGLE = os.environ['FRONT_GOOGLE']
BACK_GOOGLE = os.environ['BACK_GOOGLE']
MY_WEATHER = os.environ['MY_WEATHER']


@app.route("/")
def homepage():

    return render_template('homepage.html')


@app.route("/register", methods=["POST"])
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
def user_login():
    # this is for users logging in
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
def dashboard():
    # checks the users logged in email and displays the dashboard with their info.
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    trips = crud.get_trips_by_userid(user.user_id)
    
    # for trip in trips:
    #     if trip.leave_date > date.today():
    #         trip_countdown = datetime.date(trip.leave_date) - datetime.date.today()
    #     return(f"Your trip to {trip.to_dest} is in: {trip} days")
    
    return render_template("user_dashboard.html", trips=trips, user=user)


@app.route("/map")
def map():
    # displays the map page
    return render_template("map.html", FRONT_GOOGLE=FRONT_GOOGLE)


@app.route("/map", methods=["POST"])
def map_post():
    # grabs the information the user puts in for their destination to post to google
    from_dest = request.json.get('from')
    to_dest = request.json.get('to')

    return redirect('/map')


@app.route("/map/waypoints")
def get_waypoints():
    from_dest = request.args.get('from')
    print('***from',from_dest)
    to_dest = request.args.get('to')
    print('***to', to_dest)
    #if departure_date == date.today():
    google_response = requests.get(
        f"https://maps.googleapis.com/maps/api/directions/json?destination={to_dest}&origin={from_dest}&key={BACK_GOOGLE}").json()
    # weather_response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={MY_WEATHER}&q=Atlanta&aqi=no').json()

    #elif departure_date > 14 days.... not sure about this one 
    #for loop here then print to console
    # print('*******', google_response)
    leg = google_response['routes'][0]['legs'][0]
    waypoints = [leg['start_location']]
    print(waypoints)
    
    for step in leg['steps']:
        waypoints.append(step['end_location'])
    return jsonify(waypoints)

@app.route("/waypoint-weather")
def way_weather():
    q = request.args.get("q")
    weather_response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={MY_WEATHER}&q={q}&aqi=no').json()
    print(weather_response)
    forecast_text = weather_response.get('current').get('condition').get('text')
    forecast_icon = weather_response.get('current').get('condition').get('icon')    
    forecast = {"forecast_icon": forecast_icon, "forecast_text": forecast_text}
    return jsonify(forecast)

@app.route("/my-trips")
def my_trips():
 # this will populate the trips on the past trips page. need to figure out how to expand the trip to show more details or populate the details some where on the page
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    trips = crud.get_trips_by_userid(user.user_id)

    past_trip_list = []
    future_trip_list = []
    today = date.today()
    
    for trip in trips:
        if trip.return_date < today:
            print(trip)
            past_trip_list.append(trip)
            print(past_trip_list)
        elif trip.leave_date > today:
            future_trip_list.append(trip)    
        
    return render_template("my-trips.html", trips=trips, future_trip_list=future_trip_list, past_trip_list=past_trip_list) #TODO fix to trip_list

# Create new trips
@app.route("/my-trips/create-trip", methods=["POST"])
def create_my_trips():
    leave_date = request.json.get('depart_date')
    return_date = request.json.get('return_date')
    # print(leave_date,return_date)
    to_dest = request.json.get('to')
    from_dest = request.json.get('from')
    to_do = request.json.get('to_do_list_items')
    list_name = request.json.get('list_name')
    print(to_do)
    logged_in_email = session.get("user_email")
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
    return redirect ("/my-trips")


# @app.route("/my-trips/upcoming-trips") #TODO: combine with the my trips
# def upcoming_trip():

#     logged_in_email = session.get("user_email")
#     user = crud.get_user_by_email(logged_in_email)
#     trips = crud.get_trips_by_userid(user.user_id)

#     trip_list = []
#     today = date.today()
#     print(today)
#     for trip in trips:
#         if trip.leave_date > today:
#             print(trip)
#             trip_list.append(trip)
           

#     return render_template("upcoming_trips.html", trips=trip_list)


@app.route("/gas-calc")
def gas():

    return render_template("gas-calc.html")


# @app.route("/to-do")
# def to_do():
# #returns the to-do template   
#     return render_template("to-do.html")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=5001)
