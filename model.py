"""Models for roadtrip companion app."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):

    __tablename__= "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False) #set password requirements

    trips = db.relationship("Trip", back_populates="user")

    def __repr__(self):
        return f'<User Table: user_id={self.user_id}, first_name={self.first_name}, email={self.email}>'

    

class Task(db.Model):

    __tablename__= "tasks"
    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'), nullable=False)
    task = db.Column(db.Text)
    completed = db.Column(db.Boolean)

    list = db.relationship("List", back_populates='tasks')

    def __repr__(self):
        return f'<Task Table: task_id={self.task_id}, task={self.task}>'


class List(db.Model):

    __tablename__= "lists"
    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'), nullable=False)
    creation_date = db.Column(db.Date) #how to do date in a table, should it be string?
    list_name = db.Column(db.String(30))

    trip = db.relationship("Trip", back_populates='lists')
    tasks = db.relationship("Task", back_populates='list')

    def __repr__(self):
        return f'<List Table: list_id={self.list_id}, trip_id={self.trip_id}>'


class Trip(db.Model):

    __tablename__= "trips"
    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    leave_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    distance = db.Column(db.Integer)
    to_dest = db.Column(db.String(50))
    from_dest = db.Column(db.String(50))
    cost = db.Column(db.Float) #AttributeError: 'SQLAlchemy' object has no attribute 'Decimal'
    budget = db.Column(db.Float) #AttributeError: 'SQLAlchemy' object has no attribute 'Decimal'

    user = db.relationship("User", back_populates="trips")
    lists = db.relationship("List", back_populates="trip")

    # def __repr__(self):
    #     return f'<Trip Table: trip_id={self.trip_id}, user_id={self.user_id}>'


def connect_to_db(flask_app):
    """Connect the database to our Flask app."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///trips"
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
