from flask import Flask, request, jsonify, redirect, render_template
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
import shortuuid

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://geetika:1234@cluster0.t02dpec.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Home page (URL input form)
@app.route('/')
def index():
    return render_template('index.html')

# API to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form.get('original_url')
    expiry_days = int(request.form.get('expiry_days', 30))
    short_code = shortuuid.uuid()[:6]
    now = datetime.utcnow()

    mongo.db.urls.insert_one({
        "original_url": original_url,
        "short_code": short_code,
        "clicks": 0,
        "created_at": now,
        "expiry_date": now + timedelta(days=expiry_days)
    })

    return render_template('result.html', short_url=request.host_url + short_code)

# Redirect short URL
@app.route('/<short_code>')
def redirect_short_url(short_code):
    url_data = mongo.db.urls.find_one({"short_code": short_code})

    if url_data:
        if datetime.utcnow() > url_data["expiry_date"]:
            return "This short URL has expired.", 410
        mongo.db.urls.update_one({"short_code": short_code}, {"$inc": {"clicks": 1}})
        return redirect(url_data["original_url"])
    return "URL not found", 404

# Dashboard page UI
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Dashboard data API
@app.route('/dashboard/data', methods=['GET'])
def dashboard_data():
    urls = mongo.db.urls.find()
    result = []
    for url in urls:
        result.append({
            "original_url": url.get("original_url", "N/A"),
            "short_url": request.host_url + url.get("short_code", ""),
            "clicks": url.get("clicks", 0),
            "created_at": url.get("created_at", datetime.utcnow()).strftime('%Y-%m-%d %H:%M'),
            "expiry_date": url.get("expiry_date", datetime.utcnow()).strftime('%Y-%m-%d %H:%M'),
            "is_expired": datetime.utcnow() > url.get("expiry_date", datetime.utcnow())
        })
    return jsonify(result)

# Run locally
if __name__ == '__main__':
    app.run(debug=True)
