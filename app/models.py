from datetime import timedelta
from bson.objectid import ObjectId

def insert_url(collection, code, original, created_at, expiry_minutes):
    expiry_time = created_at + timedelta(minutes=expiry_minutes)
    doc = {
        "short_code": code,
        "original_url": original,
        "created_at": created_at,
        "expiry": expiry_time,
        "clicks": 0
    }
    collection.insert_one(doc)

def get_url_data(collection, code):
    return collection.find_one({"short_code": code})

def update_click(collection, code):
    collection.update_one({"short_code": code}, {"$inc": {"clicks": 1}})
