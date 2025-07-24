from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import timedelta

mongo = PyMongo()
client = MongoClient('mongodb://localhost:27017/')
db = client['url_shortener']
collection = db['urls']

def create_app():
    app = Flask(__name__)
    
    # MongoDB config
    app.config["MONGO_URI"] = "mongodb://localhost:27017/url_shortener"
    
    mongo.init_app(app)

    # Register routes
    from .routes import shortener
    app.register_blueprint(shortener)

    return app
