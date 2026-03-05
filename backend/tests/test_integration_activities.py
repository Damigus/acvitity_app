# testy integracyjne dla wpisow
import random

def test_dodawanie_i_usuwanie_wpisu(client):
    losowa_nazwa = f"Kino {random.randint(1, 10000)}"
    user = "TEST_uczen"
    
    # dodajemy nowy wpis na wyjscie
    odp = client.post('/activity', json={
        "username": user,
        "name": losowa_nazwa,
        "description": "Film 365 dni",
        "city": "Warszawa",
        "planned_date": "2026-03-10",
        "planned_time": "18:00"
    })
    assert odp.status_code == 200
    
    # pobieramy wpisy i szukamy naszego bo w bazie moga byc inne
    odp_get = client.get('/activity')
    dane = odp_get.json
    
    nasz_wpis = None
    for wpis in dane:
        if wpis["name"] == losowa_nazwa:
            nasz_wpis = wpis
            break
            
    assert nasz_wpis is not None
    wpis_id = nasz_wpis["_id"]
    
    # probujemy usunac jako inny user nie powinno sie udac
    odp_zle_usuniecie = client.delete(f'/activity/{wpis_id}', headers={'x-username': 'TEST_ktos_inny'})
    assert odp_zle_usuniecie.status_code == 403
    
    # usuwamy poprawnie jako autor
    odp_dobre_usuniecie = client.delete(f'/activity/{wpis_id}', headers={'x-username': user})
    assert odp_dobre_usuniecie.status_code == 200
    
    # sprawdzamy czy na pewno zniknelo
    odp_get2 = client.get('/activity')
    czy_istnieje = any(w["_id"] == wpis_id for w in odp_get2.json)
    assert czy_istnieje == False

def test_edycja_wpisu_innego_usera(client):
    # sprawdzamy czy ktos moze zedytowac nie swoj wpis
    losowa_nazwa = f"Kino {random.randint(1, 10000)}"
    user_autor = "TEST_autor"
    user_haker = "TEST_haker"
    
    client.post('/activity', json={
        "username": user_autor,
        "name": losowa_nazwa,
        "city": "Warszawa"
    })
    
    dane = client.get('/activity').json
    wpis_id = next(w for w in dane if w["name"] == losowa_nazwa)["_id"]
    
    # proba edycji przez tigera bonzo
    odp_edycja = client.put(f'/activity/{wpis_id}', json={
        "username": user_haker,
        "name": "Zhakowane kino",
        "city": "Warszawa"
    })
    # powinno wywalic blad 403 brak uprawnien
    assert odp_edycja.status_code == 403

def test_lajkowanie_wpisu(client):
    losowa_nazwa = f"Planszowki {random.randint(1, 10000)}"
    user = "TEST_gracz"
    
    client.post('/activity', json={
        "username": user,
        "name": losowa_nazwa,
        "city": "Warszawa"
    })
    
    wpis_id = next(w for w in client.get('/activity').json if w["name"] == losowa_nazwa)["_id"]
    
    # dajemy lajka
    client.post(f'/activity/{wpis_id}/like', json={"username": "TEST_kolega"})
    
    # sprawdzamy czy lajk wszedl
    wpis_po_lajku = next(w for w in client.get('/activity').json if w["_id"] == wpis_id)
    assert wpis_po_lajku["likes_count"] == 1
    assert "TEST_kolega" in wpis_po_lajku["liked_by"]
    
    # klikamy jeszcze raz lajk powinien zniknac
    client.post(f'/activity/{wpis_id}/like', json={"username": "TEST_kolega"})
    wpis_po_odlajkowaniu = next(w for w in client.get('/activity').json if w["_id"] == wpis_id)
    assert wpis_po_odlajkowaniu["likes_count"] == 0
