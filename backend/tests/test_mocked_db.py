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


def wczytaj_dane(sciezka):
    """Wczytuje dane z pliku JSON"""
    with open(sciezka, 'r') as f:
        return json.load(f)

def stworz_baze_z_pliku():
    """Tworzy prosty obiekt, który udaje bazę danych na podstawie pliku JSON"""
    dane_z_pliku = wczytaj_dane(USERS_FILE)
    
    # Lista na dane, które "zapiszemy" w trakcie testu
    zapisane_w_tescie = []

    # Udajemy funkcję find_one
    def udawane_find_one(szukane):
        for u in dane_z_pliku:
            # Sprawdzamy czy username i password pasują
            if all(u.get(k) == v for k, v in szukane.items()):
                return u
        return None

    # Udajemy funkcję insert_one
    def udawane_insert_one(nowy_obiekt):
        zapisane_w_tescie.append(nowy_obiekt)

    users_mock = type('Users', (), {'find_one': udawane_find_one, 'insert_one': udawane_insert_one})
    return type('Database', (), {'users': users_mock, 'zapisane': zapisane_w_tescie})

# --- TESTY LOGOWANIA (PARAMETRYZOWANE) ---

@pytest.mark.parametrize("login, haslo, spodziewany_kod", [
    ("adam", "123", 200),        # Adam jest w pliku i ma dobre hasło
    ("jan", "haslo_jana", 200),  # Jan też jest w pliku
    ("adam", "zle_haslo", 401),  # Złe hasło dla Adama
    ("ktos_inny", "123", 401),   # Tego usera nie ma w pliku
])
def test_jednostkowy_logowanie(login, haslo, spodziewany_kod):
    """Testujemy logowanie bezpośrednio wywołując funkcję logiczną"""
    baza = stworz_baze_z_pliku()
    wynik, kod = sprawdz_logowanie(baza, login, haslo)
    assert kod == spodziewany_kod

# --- TESTY REJESTRACJI (PARAMETRYZOWANE) ---

@pytest.mark.parametrize("nowy_login, czy_zajety", [
    ("adam", True),        # Adam już jest w users.json
    ("marek", True),       # Marek też jest
    ("nowy_uczen", False), # Tego nie ma w pliku
])
def test_jednostkowy_rejestracja(nowy_login, czy_zajety):
    """Testujemy rejestrację: czy system widzi kto już istnieje"""
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
    """Testujemy czy funkcja czytająca pogodę z pliku działa"""
    pogoda_z_pliku = wczytaj_dane(WEATHER_FILE)
    miasto = "Warszawa"
    assert pogoda_z_pliku[miasto]["temperature"] == 15

def test_jednostkowy_dodawanie_aktywnosci():
    """Testujemy logikę tworzenia nowej aktywności z pogodą"""
    # Udajemy funkcję pogodową, która czyta z naszego pliku JSON
    def udawana_pogoda(miasto, data, czas):
        dane = wczytaj_dane(WEATHER_FILE)
        return dane.get(miasto, {"temperature": 0})

    # Wywołujemy funkcję logiczną z activities.py
    nowa_act = przygotuj_aktywnosc(
        "adam", "Bieganie", "Warszawa", "Fajny trening", 
        "2026-03-04", "10:00", udawana_pogoda
    )
    
    # Sprawdzamy czy dane się zgadzają (temperatura 15 jest w weather.json dla Warszawy)
    assert nowa_act["name"] == "Bieganie"
    assert nowa_act["temperature"] == 15
    assert nowa_act["username"] == "adam"

