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

# Create a new user
@app.route("/users", methods=["POST"])
def register_user():
    fname = request.form.get("first name")
    lname = request.form.get("last name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_pw = request.form.get("confirm password")
    user = crud.get_user_by_email(email)
        
    if user:
        flash("This email alreadys exists. Please log in.")
    else:
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user) #can this go in crud as a part of the function or does it need to be here
        db.session.commit()
        flash("Account created successfuly! Please log in.")

    return redirect('/')



# this is for users logging in
@app.route("/dashboard", methods=["POST"])
def user_dashboard():

    email = request.form.get("email") 
    password = request.form.get("password")

    user = crud.get_user_by_email(email) #this isn't working. 
    print(user)

    if not user or user.password != password: #so this isn't working
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
    

    # name = user.first_name
    return render_template('user_dashboard.html')


















if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)