from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
import json
from jinja2 import StrictUndefined
import os
import requests
from datetime import date

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

MY_GOOGLE = os.environ['MY_GOOGLE']


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
    print(user)
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
    
    return render_template("user_dashboard.html", trips=trips, user=user)


@app.route("/map")
def map():
    # displays the map page
    return render_template("map.html")


@app.route("/map", methods=["POST"])
def map_post():
    # grabs the information the user puts in for their destination to post to google
    from_dest = request.form.get('from')
    to_dest = request.form.get('to')

    response = requests.get(
        f"https://maps.googleapis.com/maps/api/directions/json?destination={to_dest}&origin={from_dest}&key={MY_GOOGLE}")
  
    return redirect('/map')


@app.route("/map/response")
def get_map_route():
    # returns the info from google to display on the map

    return redirect('/map')


@app.route("/past-trips")
def past_trips():
 # this will populate the trips on the past trips page. need to figure out how to expand the trip to show more details or populate the details some where on the page
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    trips = crud.get_trips_by_userid(user.user_id)

    trip_list = []
    today = date.today()
    
    for trip in trips:
        if trip.return_date < today:
            print(trip)
            trip_list.append(trip)
            print(trip_list)
            trip_list.sort()
        

    return render_template("past_trips.html", trips=trip_list)

@app.route("/upcoming-trips")
def upcoming_trip():

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    trips = crud.get_trips_by_userid(user.user_id)

    trip_list = []
    today = date.today()
    print(today)
    for trip in trips:
        if trip.leave_date > today:
            print(trip)
            trip_list.append(trip)
           

    return render_template("upcoming_trips.html", trips=trip_list)


@app.route("/gas-calc")
def gas():

    return render_template("gas-calc.html")


@app.route("/to-do")
def to_do():
#returns the to-do template   
    return render_template("to-do.html")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="127.0.0.1", debug=True)
