from flask import Blueprint, request, jsonify, redirect, render_template, current_app
from datetime import datetime, timedelta
from .utils import generate_short_code, is_valid_url

shortener = Blueprint('shortener', __name__)

@shortener.route('/', methods=['GET'])
def home():
    return jsonify({"message": "URL Shortener is running!"})


@shortener.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    expiry_days = data.get('expiry_days', 30)

    if not original_url or not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = generate_short_code()
    expiry_date = datetime.utcnow() + timedelta(days=expiry_days)

    current_app.db.urls.insert_one({
        'original_url': original_url,
        'short_code': short_code,
        'created_at': datetime.utcnow(),
        'expiry_date': expiry_date,
        'clicks': 0
    })

    return jsonify({'short_url': request.host_url + short_code}), 200


@shortener.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    record = current_app.db.urls.find_one({'short_code': short_code})
    if not record:
        return jsonify({'error': 'Invalid short code'}), 404

    if record['expiry_date'] < datetime.utcnow():
        return jsonify({'error': 'Link expired'}), 410

    current_app.db.urls.update_one({'short_code': short_code}, {'$inc': {'clicks': 1}})
    return redirect(record['original_url'])


@shortener.route('/analytics/<short_code>', methods=['GET'])
def analytics(short_code):
    record = current_app.db.urls.find_one({'short_code': short_code})
    if not record:
        return jsonify({'error': 'Invalid short code'}), 404

    return jsonify({
        'original_url': record['original_url'],
        'short_code': short_code,
        'clicks': record['clicks'],
        'expiry_date': record['expiry_date'],
        'created_at': record['created_at']
    })


@shortener.route('/dashboard/data', methods=['GET'])
def get_all_urls():
    urls = current_app.db.urls.find()
    result = []
    for url in urls:
        short_code = url.get("short_code")
        if not short_code:
            continue

        result.append({
            "original_url": url.get("original_url", "N/A"),
            "short_url": request.host_url + short_code,
            "clicks": url.get("clicks", 0),
            "created_at": url.get("created_at").strftime('%Y-%m-%d %H:%M') if url.get("created_at") else "N/A",
            "expiry_date": url.get("expiry_date").strftime('%Y-%m-%d %H:%M') if url.get("expiry_date") else "N/A",
            "is_expired": datetime.utcnow() > url["expiry_date"] if url.get("expiry_date") else False
        })
    return jsonify(result)


@shortener.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')
