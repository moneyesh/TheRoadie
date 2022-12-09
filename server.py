from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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
            db.session.add(user) #can this go in crud as a part of the function or does it need to be here
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
   
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    trips = crud.get_trips_by_userid(user.user_id)
    print('*************',trips)

    return render_template("user_dashboard.html", trips=trips, user=user)













if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)