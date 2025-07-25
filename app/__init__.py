from flask import Flask
from pymongo import MongoClient
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.permanent_session_lifetime = timedelta(days=5)

    # Setup MongoDB
    client = MongoClient("mongodb+srv://geetika:1234@cluster0.t02dpec.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["urlDB"]

    # Store DB reference in app
    app.db = db

    return app
