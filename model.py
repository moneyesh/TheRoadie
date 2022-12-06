"""Models for roadtrip companion app."""

from flask_sqlalchemy import SQLAlchemy\

db = SQLAlchemy()

class User(db.model):

    __tablename__= "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(15), nullable=False)
