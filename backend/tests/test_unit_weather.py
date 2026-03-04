import pytest
import sys
import os

# dodajemy backend do sciezki zeby zaimportowac weather
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.weather import get_weather_data

# testy parametryzowane sprawdzamy rozne dziwne miasta ktorych nie mamy na liscie
# laczymy sie z prawdziwym api bez mockowania
@pytest.mark.parametrize("dziwne_miasto", ["Radom", "Sosnowiec", "Nibylandia"])
def test_nieznane_miasto_prawdziwe_api(dziwne_miasto):
    # jak podamy miasto spoza listy to kod domyslnie bierze warszawe
    wynik = get_weather_data(dziwne_miasto)
    
    # skoro to prawdziwe api nie wiemy jaka jest dokladnie temperatura bo sie zmienia
    # ale wiemy ze musi byc liczba int lub float i klucze musza istniec
    assert "temperature" in wynik
    assert isinstance(wynik["temperature"], (int, float))
    assert "windspeed" in wynik
    assert isinstance(wynik["windspeed"], (int, float))
    assert "precipitation" in wynik

def test_zla_data_przeszlosc_prawdziwe_api():
    # dajemy date z przeszlosci
    # prawdziwe api nie ma prognozy na 1999 rok w darmowym planie
    wynik = get_weather_data("Warszawa", "1999-01-01", "12:00")
    
    # nasz kod w weather py w razie braku daty w time zwraca same zera
    assert wynik["temperature"] == 0
    assert wynik["windspeed"] == 0
    assert wynik["precipitation"] == 0
