from flask import Flask, jsonify, request, render_template
from bson.json_util import dumps
from datetime import datetime
from app import create_app, collection  # Make sure collection is imported from your app
                                         # or wherever you initialized MongoDB

app = create_app()

# Route to get all URL data (for dashboard)
@app.route('/dashboard/data', methods=['GET'])
def get_all_urls():
    urls = collection.find()
    result = []
    for url in urls:
        result.append({
            "original_url": url["original_url"],
            "short_url": request.host_url + url["short_code"],
            "clicks": url.get("clicks", 0),
            "created_at": url["created_at"].strftime('%Y-%m-%d %H:%M'),
            "expiry_date": url["expiry_date"].strftime('%Y-%m-%d %H:%M'),
            "is_expired": datetime.utcnow() > url["expiry_date"]
        })
    return jsonify(result)

# Route to serve the dashboard UI
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
