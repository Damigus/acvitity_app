from flask import Blueprint, request, jsonify
from database import get_db

auth_bp = Blueprint('auth', __name__)
db = get_db()

@auth_bp.route('/register', methods=['POST'])
def register():
    if db is None: return jsonify({"error": "brak polaczenia z baza"}), 500
    data = request.json
    if db.users.find_one({"username": data['username']}):
        return jsonify({"error": "uzytkownik istnieje"}), 400
    db.users.insert_one({"username": data['username'], "password": data['password']})
    return jsonify({"success": True})

@auth_bp.route('/login', methods=['POST'])
def login():
    if db is None: return jsonify({"error": "brak polaczenia z baza"}), 500
    data = request.json
    user = db.users.find_one({"username": data['username'], "password": data['password']})
    if user:
        return jsonify({"success": True, "username": data['username']})
    return jsonify({"error": "bledne dane"}), 401
