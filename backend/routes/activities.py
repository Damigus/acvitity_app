from flask import Blueprint, request, jsonify
from database import get_db
from utils.weather import get_weather_data
from datetime import datetime
from bson.objectid import ObjectId

activities_bp = Blueprint('activities', __name__)
db = get_db()

# --- LOGIKA BIZNESOWA (to testujemy jednostkowo) ---

def przygotuj_aktywnosc(username, name, city, description, planned_date, planned_time, weather_func):
    """Tworzy słownik z nową aktywnością, pobierając pogodę"""
    weather = weather_func(city, planned_date, planned_time)
    
    return {
        "username": username,
        "name": name,
        "description": description or '',
        "city": city,
        "planned_date": planned_date or '',
        "planned_time": planned_time or '',
        "temperature": weather.get('temperature', 0),
        "windspeed": weather.get('windspeed', 0),
        "precipitation": weather.get('precipitation', 0),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# --- ENDPOINTY ---

@activities_bp.route('', methods=['GET'])
def get_activities():
    if db is None: return jsonify([])
    all_acts = list(db.activities.find().sort("timestamp", -1))
    for act in all_acts:
        act['_id'] = str(act['_id'])
        act['likes_count'] = db.likes.count_documents({"activity_id": act['_id']})
        act['liked_by'] = [l['username'] for l in db.likes.find({"activity_id": act['_id']})]
    return jsonify(all_acts)

@activities_bp.route('', methods=['POST'])
def add_activity():
    if db is None: return jsonify({"error": "brak bazy"}), 500
    data = request.json
    
    nowa_act = przygotuj_aktywnosc(
        data['username'], 
        data['name'], 
        data['city'], 
        data.get('description'), 
        data.get('planned_date'), 
        data.get('planned_time'),
        get_weather_data
    )
    
    db.activities.insert_one(nowa_act)
    return jsonify({"success": True})

@activities_bp.route('/<id>', methods=['PUT'])
def edit_activity(id):
    if db is None: return jsonify({"error": "brak bazy"}), 500
    data = request.json
    weather = get_weather_data(data['city'], data.get('planned_date'), data.get('planned_time'))
    
    act = db.activities.find_one({"_id": ObjectId(id)})
    if act and act['username'] == data['username']:
        update_data = {
            "name": data['name'],
            "description": data.get('description', ''),
            "city": data['city'],
            "planned_date": data.get('planned_date', ''),
            "planned_time": data.get('planned_time', ''),
            "temperature": weather.get('temperature', 0),
            "windspeed": weather.get('windspeed', 0),
            "precipitation": weather.get('precipitation', 0)
        }
        db.activities.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        return jsonify({"success": True})
    return jsonify({"error": "brak uprawnien"}), 403

@activities_bp.route('/<id>', methods=['DELETE'])
def delete_activity(id):
    if db is None: return jsonify({"error": "brak bazy"}), 500
    username = request.headers.get('x-username')
    act = db.activities.find_one({"_id": ObjectId(id)})
    if act and act['username'] == username:
        db.activities.delete_one({"_id": ObjectId(id)})
        db.likes.delete_many({"activity_id": id})
        return jsonify({"success": True})
    return jsonify({"error": "brak uprawnien"}), 403

@activities_bp.route('/<id>/like', methods=['POST'])
def toggle_like(id):
    if db is None: return jsonify({"error": "brak bazy"}), 500
    data = request.json
    existing = db.likes.find_one({"activity_id": id, "username": data['username']})
    if existing:
        db.likes.delete_one({"activity_id": id, "username": data['username']})
    else:
        db.likes.insert_one({"activity_id": id, "username": data['username']})
    return jsonify({"success": True})
