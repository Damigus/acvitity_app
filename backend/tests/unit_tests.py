import pytest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes.auth import sprawdz_rejestracje, sprawdz_logowanie
from routes.activities import przygotuj_aktywnosc

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

    def udawane_find_one(szukane):
        for u in dane_z_pliku:
            if all(u.get(k) == v for k, v in szukane.items()):
                return u
        return None

    # Udajemy funkcję insert_one
    def udawane_insert_one(nowy_obiekt):
        zapisane_w_tescie.append(nowy_obiekt)


    class PustyObiekt:
        pass

    baza = PustyObiekt()
    baza.users = PustyObiekt()
    
    # Doczepiamy nasze udawane funkcje i listę do obiektu
    baza.users.find_one = udawane_find_one
    baza.users.insert_one = udawane_insert_one
    baza.zapisane = zapisane_w_tescie
    
    return baza

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


def test_jednostkowy_pogoda_z_pliku():
    """Testujemy czy funkcja czytająca pogodę z pliku działa"""
    pogoda_z_pliku = wczytaj_dane(WEATHER_FILE)
    miasto = "Warszawa"
    assert pogoda_z_pliku[miasto]["temperature"] == 15

def test_jednostkowy_dodawanie_aktywnosci():
    """Testujemy logikę tworzenia nowej aktywności z pogodą (ręczna podmiana)"""
    def udawana_pogoda(miasto, data, czas):
        dane = wczytaj_dane(WEATHER_FILE)
        return dane.get(miasto, {"temperature": 0})

    import routes.activities
    oryginalna_funkcja = routes.activities.get_weather_data # Zapisujemy oryginał!
    routes.activities.get_weather_data = udawana_pogoda     # Podmieniamy na naszą

    try:
        nowa_act = przygotuj_aktywnosc(
            "adam", "Bieganie", "Warszawa", "Fajny trening", 
            "2026-03-04", "10:00"
        )
        
        assert nowa_act["name"] == "Bieganie"
        assert nowa_act["temperature"] == 15
        assert nowa_act["username"] == "adam"
    finally:

        routes.activities.get_weather_data = oryginalna_funkcja

