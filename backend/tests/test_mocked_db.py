import pytest
from unittest.mock import patch
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
