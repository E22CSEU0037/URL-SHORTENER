from flask import Flask, jsonify, request, render_template
from bson.json_util import dumps
from datetime import datetime
from app import create_app, collection 
# Make sure collection is imported from your app
                                         # or wherever you initialized MongoDB
from flask import Flask, request, jsonify, redirect, render_template
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
import shortuuid

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://geetika:1234@cluster0.t02dpec.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)


app = create_app()

@app.route('/dashboard')
def get_all_urls():
    all_urls = mongo.db.urls.find()
    url_list = []
    for url in all_urls:
        url_list.append({
            "original_url": url["original_url"],
            "short_id": url["short_id"],
            "created_at": url["created_at"],
            "clicks": url["clicks"],
            "expires_at": url["expires_at"]
        })
    return render_template("dashboard.html", urls=url_list)

# Route to get all URL data (for dashboard)
@app.route('/dashboard/data', methods=['GET'])
def get_all_urls():
    urls = collection.find()
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


# Route to serve the dashboard UI
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
