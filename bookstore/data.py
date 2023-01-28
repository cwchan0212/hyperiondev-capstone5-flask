# Create database
# flask --app bookstore/data run

from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from bookstore import app
from .models import db

try:
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables created successfully.")
except Exception as e:
    print("An error occurred while creating the tables:", e)

