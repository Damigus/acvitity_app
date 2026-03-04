import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# dodajemy backend do sciezki
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- TESTY DLA SYTUACJI GDY BAZA LEZY ---

# mockujemy baze danych udajemy ze serwer bazy padl i zwraca none
# patchujemy db w pliku auth
@patch('routes.auth.db', None)
def test_logowanie_gdy_baza_lezy(client):
    odp = client.post('/api/login', json={
        "username": "ktokolwiek",
        "password": "123"
    })
    # nasz kod w auth py ma if db is none return jsonify error brak polaczenia z baza 500
    assert odp.status_code == 500
    assert odp.json["error"] == "brak polaczenia z baza"

# patchujemy db w pliku activities
@patch('routes.activities.db', None)
def test_pobieranie_aktywnosci_gdy_baza_lezy(client):
    odp = client.get('/activity')
    # nasz kod w activities py ma if db is none return jsonify pusta lista
    assert odp.status_code == 200
    assert odp.json == []

# --- TESTY JEDNOSTKOWE Z ZMOCKOWANA BAZA DANYCH ---

def test_logowanie_poprawne(client):
    mock_db = MagicMock()
    mock_db.users.find_one.return_value = {"username": "testuser", "password": "123"}
    
    with patch('routes.auth.db', mock_db):
        odp = client.post('/api/login', json={
            "username": "testuser",
            "password": "123"
        })
        assert odp.status_code == 200
        assert odp.json["success"] is True
        assert odp.json["username"] == "testuser"

def test_logowanie_bledne_dane(client):
    mock_db = MagicMock()
    mock_db.users.find_one.return_value = None
    
    with patch('routes.auth.db', mock_db):
        odp = client.post('/api/login', json={
            "username": "testuser",
            "password": "zle_haslo"
        })
        assert odp.status_code == 401
        assert odp.json["error"] == "bledne dane"

def test_rejestracja_nowy_user(client):
    mock_db = MagicMock()
    mock_db.users.find_one.return_value = None
    
    with patch('routes.auth.db', mock_db):
        odp = client.post('/api/register', json={
            "username": "nowy_user",
            "password": "123"
        })
        assert odp.status_code == 200
        assert odp.json["success"] is True
        mock_db.users.insert_one.assert_called_once_with({"username": "nowy_user", "password": "123"})

def test_rejestracja_istniejacy_user(client):
    mock_db = MagicMock()
    mock_db.users.find_one.return_value = {"username": "istniejacy_user"}
    
    with patch('routes.auth.db', mock_db):
        odp = client.post('/api/register', json={
            "username": "istniejacy_user",
            "password": "123"
        })
        assert odp.status_code == 400
        assert odp.json["error"] == "uzytkownik istnieje"
        mock_db.users.insert_one.assert_not_called()

def test_pobieranie_aktywnosci_poprawne(client):
    mock_db = MagicMock()
    
    # mockujemy kursor bazy danych (find().sort())
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = [
        {"_id": "123456789012345678901234", "name": "Bieganie", "username": "testuser"}
    ]
    mock_db.activities.find.return_value = mock_cursor
    
    # mockujemy liczbe lajkow i kto polubil
    mock_db.likes.count_documents.return_value = 2
    mock_db.likes.find.return_value = [{"username": "user1"}, {"username": "user2"}]
    
    with patch('routes.activities.db', mock_db):
        odp = client.get('/activity')
        assert odp.status_code == 200
        assert len(odp.json) == 1
        assert odp.json[0]["name"] == "Bieganie"
        assert odp.json[0]["likes_count"] == 2
        assert odp.json[0]["liked_by"] == ["user1", "user2"]

def test_dodawanie_aktywnosci(client):
    mock_db = MagicMock()
    
    # mockujemy baze danych oraz zewnetrzne API pogodowe
    with patch('routes.activities.db', mock_db), \
         patch('routes.activities.get_weather_data', return_value={"temperature": 20, "windspeed": 5, "precipitation": 0}):
        
        odp = client.post('/activity', json={
            "username": "testuser",
            "name": "Rower",
            "city": "Warszawa"
        })
        assert odp.status_code == 200
        assert odp.json["success"] is True
        mock_db.activities.insert_one.assert_called_once()
        
        # sprawdzamy czy argument przekazany do insert_one zawiera odpowiednie dane
        inserted_data = mock_db.activities.insert_one.call_args[0][0]
        assert inserted_data["name"] == "Rower"
        assert inserted_data["city"] == "Warszawa"
        assert inserted_data["temperature"] == 20
