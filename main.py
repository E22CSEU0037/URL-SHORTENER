from flask import Flask, request, redirect, render_template, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import string, random, datetime, os

# Flask app setup
app = Flask(__name__, template_folder=os.path.join('app', 'templates'))

# MongoDB setup
client = MongoClient("mongodb+srv://geetika:1234@cluster0.t02dpec.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Update if you're using Atlas or Render
db = client["url_shortener"]
collection = db["urls"]

# Utility: generate short ID
def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

# Home page with form
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Create shortened URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    original_url = request.form["original_url"]
    short_id = generate_short_id()

    while collection.find_one({"short_id": short_id}):
        short_id = generate_short_id()

    data = {
        "original_url": original_url,
        "short_id": short_id,
        "created_at": datetime.datetime.utcnow(),
        "clicks": 0
    }
    collection.insert_one(data)

    short_url = request.host_url + short_id
    return render_template("index.html", short_url=short_url)

# Redirect to original URL
@app.route("/<short_id>")
def redirect_url(short_id):
    url_entry = collection.find_one({"short_id": short_id})
    if url_entry:
        collection.update_one({"short_id": short_id}, {"$inc": {"clicks": 1}})
        return redirect(url_entry["original_url"])
    return "URL not found", 404

@app.route("/dashboard")
def dashboard():
    data = list(collection.find({}, {"_id": 0}))
    return render_template("dashboard.html", data=data)


# Analytics dashboard (JSON response for now)
@app.route("/analytics", methods=["GET"])
def analytics():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
