from flask import Flask
from flask_pymongo import PyMongo
from datetime import timedelta

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb+srv://geetika:1234@cluster0.t02dpec.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    app.secret_key = "your-secret-key"
    app.permanent_session_lifetime = timedelta(days=5)

    mongo.init_app(app)

    # 🔁 Import after initializing app and mongo
    from .routes import app_routes
    app.register_blueprint(app_routes)

    return app
