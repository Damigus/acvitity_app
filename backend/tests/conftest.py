import pytest
import os
import sys

# dodajemy folder backend do sciezki zeby testy widzialy nasze pliki
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import get_db

@pytest.fixture
def client():
    # uzywamy prawdziwej bazy danych z dockera
    if "MONGO_URI" not in os.environ:
        os.environ["MONGO_URI"] = "mongodb://localhost:27017/"
    
    # wlaczamy tryb testowy we flasku
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client
        
    # sprzatanie smieci po testach
    # usuwamy tylko te dokumenty w ktorych nazwa uzytkownika zaczyna sie od TEST_
    db = get_db()
    if db is not None:
        db.users.delete_many({"username": {"$regex": "^TEST_"}})
        db.activities.delete_many({"username": {"$regex": "^TEST_"}})
        db.likes.delete_many({"username": {"$regex": "^TEST_"}})
