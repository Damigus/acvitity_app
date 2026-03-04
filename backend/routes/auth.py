from flask import Blueprint, request, jsonify
from database import get_db

auth_bp = Blueprint('auth', __name__)
db = get_db()


def sprawdz_rejestracje(db_mock, username, password):
    """sprawdzamy czy user juz istnieje"""
    if db_mock.users.find_one({"username": username}):
        return {"error": "uzytkownik istnieje"}, 400
    
    db_mock.users.insert_one({"username": username, "password": password})
    return {"success": True}, 200

def sprawdz_logowanie(db_mock, username, password):
    """sprawdzamy czy w bazie danych sa dane do logowania"""
    user = db_mock.users.find_one({"username": username, "password": password})
    if user:
        return {"success": True, "username": username}, 200
    return {"error": "bledne dane"}, 401

@auth_bp.route('/register', methods=['POST'])
def register():
    if db is None: return jsonify({"error": "brak polaczenia z baza"}), 500
    data = request.json
    wynik, kod = sprawdz_rejestracje(db, data['username'], data['password'])
    return jsonify(wynik), kod

@auth_bp.route('/login', methods=['POST'])
def login():
    if db is None: return jsonify({"error": "brak polaczenia z baza"}), 500
    data = request.json
    wynik, kod = sprawdz_logowanie(db, data['username'], data['password'])
    return jsonify(wynik), kod
