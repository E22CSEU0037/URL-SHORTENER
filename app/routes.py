from flask import Blueprint, request, render_template, redirect, url_for
from datetime import datetime, timedelta
import shortuuid
from . import mongo  # ✅ This now works because __init__.py has already initialized mongo

app_routes = Blueprint("app_routes", __name__)

@app_routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        expiry_days = int(request.form.get("expiry_days", 7))

        short_code = shortuuid.ShortUUID().random(length=6)
        expiry_date = datetime.utcnow() + timedelta(days=expiry_days)

        mongo.db.urls.insert_one({
            "original_url": original_url,
            "short_code": short_code,
            "created_at": datetime.utcnow(),
            "expiry_date": expiry_date,
            "clicks": 0
        })

        return render_template("index.html", short_url=request.host_url + short_code)

    return render_template("index.html")

@app_routes.route('/<short_code>')
def redirect_url(short_code):
    url_data = mongo.db.urls.find_one({"short_code": short_code})
    if url_data:
        if datetime.utcnow() < url_data["expiry_date"]:
            mongo.db.urls.update_one({"short_code": short_code}, {"$inc": {"clicks": 1}})
            return redirect(url_data["original_url"])
        else:
            return "Link expired"
    return "Invalid URL"

@app_routes.route('/dashboard')
def dashboard():
    urls = mongo.db.urls.find()
    url_list = []
    for url in urls:
        url_list.append({
            "original_url": url.get("original_url"),
            "short_code": url.get("short_code"),
            "clicks": url.get("clicks", 0),
            "created_at": url.get("created_at").strftime("%Y-%m-%d %H:%M"),
            "expiry_date": url.get("expiry_date").strftime("%Y-%m-%d %H:%M"),
            "expired": datetime.utcnow() > url.get("expiry_date")
        })
    return render_template("dashboard.html", urls=url_list)
