# testy integracyjne dla logowania i rejestracji
# uzywamy prawdziwej bazy danych
import random

def test_rejestracja_i_logowanie(client):
    # dodajemy losowy numerek do nazwy bo na bazie produkcyjnej
    # ten user moze juz istniec po pierwszym odpaleniu testow
    losowy_user = f"TEST_uczen_{random.randint(1, 10000)}"
    
    # rejestrujemy nowego usera
    odp = client.post('/api/register', json={
        "username": losowy_user,
        "password": "trudne_haslo123"
    })
    # kod 200 znaczy ze wszystko ok
    assert odp.status_code == 200
    assert odp.json["success"] == True

    # logujemy sie poprawnym haslem
    odp2 = client.post('/api/login', json={
        "username": losowy_user,
        "password": "trudne_haslo123"
    })
    assert odp2.status_code == 200
    assert odp2.json["success"] == True

def test_rejestracja_tego_samego_usera_dwa_razy(client):
    user = f"TEST_klon_{random.randint(1, 10000)}"
    
    # pierwsza rejestracja powinna sie udac
    client.post('/api/register', json={"username": user, "password": "123"})
    
    # druga rejestracja na ten sam login powinna wywalic blad
    odp = client.post('/api/register', json={"username": user, "password": "123"})
    assert odp.status_code == 400
    assert odp.json["error"] == "uzytkownik istnieje"

def test_logowanie_zle_haslo(client):
    losowy_user = f"TEST_janek_{random.randint(1, 10000)}"
    # najpierw tworzymy usera bo inaczej nie ma jak sprawdzic logowania
    client.post('/api/register', json={"username": losowy_user, "password": "123"})
    
    # probujemy wejsc na zlym hasle
    odp = client.post('/api/login', json={
        "username": losowy_user,
        "password": "zle_haslo"
    })
    # kod 401 to brak autoryzacji
    assert odp.status_code == 401
    assert odp.json["error"] == "bledne dane"

def test_logowanie_nieistniejacy_user(client):
    # probujemy zalogowac kogos kogo na bank nie ma w bazie
    odp = client.post('/api/login', json={
        "username": f"TEST_duch_{random.randint(10000, 99999)}",
        "password": "uuu"
    })
    assert odp.status_code == 401
    assert odp.json["error"] == "bledne dane"
