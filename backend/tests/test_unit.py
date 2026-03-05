import pytest
import json
import os
import sys

# Dodajemy folder backend do ścieżki, żeby Python widział nasze pliki
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importujemy funkcje, które chcemy przetestować
from routes.auth import sprawdz_rejestracje, sprawdz_logowanie
from routes.activities import przygotuj_aktywnosc

# Ścieżki do naszych plików z "udanymi" danymi
MOCK_DATA_DIR = os.path.join(os.path.dirname(__file__), 'mock_data')
USERS_FILE = os.path.join(MOCK_DATA_DIR, 'users.json')
WEATHER_FILE = os.path.join(MOCK_DATA_DIR, 'weather.json')

from unittest.mock import MagicMock

# --- POMOCNICZE FUNKCJE ---

def wczytaj_dane(sciezka):
    with open(sciezka, 'r') as f:
        return json.load(f)

def stworz_baze_z_pliku():
    dane = wczytaj_dane(USERS_FILE)
    baza = MagicMock()
    
    def find_one(szukane):
        for u in dane:
            if all(u.get(k) == v for k, v in szukane.items()):
                return u
        return None

    # podpinamy logike pod udawane metody
    baza.users.find_one.side_effect = find_one
    return baza

# --- TESTY LOGOWANIA (PARAMETRYZOWANE) ---

@pytest.mark.parametrize("login, haslo, spodziewany_kod", [
    ("adam", "123", 200),
    ("jan", "haslo_jana", 200),
    ("adam", "zle_haslo", 401),
    ("ktos_inny", "123", 401),
])
def test_jednostkowy_logowanie(login, haslo, spodziewany_kod):
    baza = stworz_baze_z_pliku()
    wynik, kod = sprawdz_logowanie(baza, login, haslo)
    assert kod == spodziewany_kod

# --- TESTY REJESTRACJI (PARAMETRYZOWANE) ---

@pytest.mark.parametrize("nowy_login, czy_zajety", [
    ("adam", True),
    ("marek", True),
    ("nowy_uczen", False),
])
def test_jednostkowy_rejestracja(nowy_login, czy_zajety):
    baza = stworz_baze_z_pliku()
    wynik, kod = sprawdz_rejestracje(baza, nowy_login, "haslo123")
    
    if czy_zajety:
        assert kod == 400
        assert wynik["error"] == "uzytkownik istnieje"
    else:
        assert kod == 200
        assert wynik["success"] is True

# --- TESTY POGODY I DODAWANIA WPISU ---

def test_jednostkowy_pogoda_z_pliku():
    pogoda_z_pliku = wczytaj_dane(WEATHER_FILE)
    miasto = "Warszawa"
    assert pogoda_z_pliku[miasto]["temperature"] == 15
    assert pogoda_z_pliku[miasto]["windspeed"] == 10
    assert pogoda_z_pliku[miasto]["precipitation"] == 0

def test_jednostkowy_dodawanie_aktywnosci():
    def udawana_pogoda(miasto, data, czas):
        dane = wczytaj_dane(WEATHER_FILE)
        return dane.get(miasto, {"temperature": 0})

    # recznie podmieniamy funkcje w module zeby nie uzywac internetu
    import routes.activities
    oryginalna_funkcja = routes.activities.get_weather_data
    routes.activities.get_weather_data = udawana_pogoda

    try:
        nowa_act = przygotuj_aktywnosc(
            "adam", "Bieganie", "Warszawa", "Fajny trening", 
            "2026-03-04", "10:00"
        )
        
        assert nowa_act["name"] == "Bieganie"
        assert nowa_act["temperature"] == 15
        assert nowa_act["windspeed"] == 10
        assert nowa_act["precipitation"] == 0
        assert nowa_act["username"] == "adam"
    finally:
        # przywracamy oryginal zeby nie psuć innych testow
        routes.activities.get_weather_data = oryginalna_funkcja

