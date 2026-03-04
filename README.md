# Activity Weather Tracker 🌤️

Aplikacja do rejestrowania i śledzenia aktywności z danymi pogodowymi. Umożliwia użytkownikom logowanie, tworzenie aktywności, planowanie ich na konkretne daty i czasy, oraz przeglądanie aktualnej pogody dla wybranych miast.

## 📋 Spis treści

- [Cechy aplikacji](#cechy-aplikacji)
- [Architektura](#architektura)
- [Wymagania](#wymagania)
- [Setup i instalacja](#setup-i-instalacja)
- [Uruchamianie aplikacji](#uruchamianie-aplikacji)
- [Struktura projektu](#struktura-projektu)
- [API Endpoints](#api-endpoints)
- [Baza danych](#baza-danych)
- [Testowanie](#testowanie)
- [Troubleshooting](#troubleshooting)

---

## ✨ Cechy aplikacji

- ✅ **Rejestracja i logowanie użytkowników** - Bezpieczne konta użytkowników
- 📍 **Śledzenie aktywności** - Twórz, edytuj, usuwaj aktywności
- 🌦️ **Integracja pogody** - Pobieranie danych pogodowych dla wybranego miasta
- 📅 **Planowanie** - Zaplanuj aktywności na konkretne daty i godziny
- 👍 **System polubień** - Polub aktywności innych użytkowników
- 🎨 **Responsywny UI** - Nowoczesny interfejs zbudowany na React + TailwindCSS

---

## 🏗️ Architektura

Projekt używa architektury **klient-serwer**:

```
┌─────────────────────────────────────────────┐
│          Frontend (React + Vite)            │
│         Localhost:5173 / Production         │
└────────────────┬────────────────────────────┘
                 │ HTTP/REST
┌────────────────▼────────────────────────────┐
│      Backend (Flask)                        │
│      Localhost:5000 / Production            │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│      MongoDB                                │
│      Localhost:27017 / Docker              │
└─────────────────────────────────────────────┘
```

### Stack techniczny:

**Backend:**
- Python 3.x
- Flask - lekki framework webowy
- Flask-CORS - obsługa CORS
- PyMongo - sterownik MongoDB
- Requests - pobieranie danych pogodowych
- Pytest - testy jednostkowe i integracyjne

**Frontend:**
- React 19 - biblioteka UI
- TypeScript - statyczne typowanie
- Vite - bundle'er/dev server
- TailwindCSS - stylowanie
- Lucide React - ikony

**Baza danych:**
- MongoDB - NoSQL baza danych

---

## 📦 Wymagania

### System:
- **Python 3.8+** (do backendu)
- **Node.js 18+** (do frontendu)
- **Docker & Docker Compose** (opcjonalnie, dla łatwego setup bazy danych)

### Zweryfikuj instalację:
```powershell
python --version
node --version
npm --version
# Jeśli korzystasz z Docker'a:
docker --version
docker-compose --version
```

---

## 🚀 Setup i instalacja

### Krok 1: Klonowanie/przygotowanie projektu

```powershell
# Przejdź do katalogu projektu
```

### Krok 2: Konfiguracja backendu

```powershell
# Przejdź do folderu backend
cd backend

# Utwórz wirtualne środowisko (zalecane)
python -m venv venv

# Aktywuj wirtualne środowisko
.\venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -r requirements.txt
```

### Krok 3: Konfiguracja MongoDB

**Opcja A: Używając Docker Compose (ZALECANE)**

```powershell
# Z głównego katalogu projektu
cd c:\Users\damia\Desktop\testowanie
docker-compose up -d
```

MongoDB będzie dostępna na `localhost:27017`

**Opcja B: MongoDB lokalnie**

Pobierz MongoDB Community Edition ze strony https://www.mongodb.com/try/download/community
i zainstaluj je

### Krok 4: Konfiguracja frontendu

```powershell
# Z głównego katalogu projektu
npm install
```

### Krok 5: Zmienne środowiskowe (opcjonalnie)

Utwórz plik `.env` w katalogu `backend/`:

```env
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/activity_db
API_PORT=5000
```

---

## ▶️ Uruchamianie aplikacji

### Development mode (z 3 terminali):

**Terminal 1 - Backend (Flask):**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
# Backend będzie dostępny na http://localhost:5000
```

**Terminal 2 - Frontend (Vite):**
```powershell
# Z głównego katalogu
npm run dev
# Frontend będzie dostępny na http://localhost:5173
```

**Terminal 3 - MongoDB (jeśli używasz Docker):**
```powershell
docker-compose up
# Baza będzie dostępna na localhost:27017
```

### Production mode:

**Build frontendu:**
```powershell
npm run build
# Wynik trafia do frontend/dist/
```

**Uruchamianie aplikacji (deploy):**
```powershell
cd backend
python app.py
```

Frontend powinien być serwowany przez reverse proxy (nginx, Apache) lub statycznie na CDN.

---

## 📁 Struktura projektu

```
testowanie/
├── README.md                          # Ten plik
├── package.json                       # Zależności frontendu
├── docker-compose.yml                 # Konfiguracja Docker'a
├── metadata.json                      # Metadane aplikacji
│
├── backend/                           # Kod backendu (Python/Flask)
│   ├── app.py                         # Główny plik aplikacji Flask
│   ├── database.py                    # Konfiguracja MongoDB
│   ├── requirements.txt               # Zależności Python
│   ├── routes/
│   │   ├── auth.py                    # Endpoints: rejestracja, logowanie
│   │   └── activities.py              # Endpoints: aktywności, polubienia
│   ├── utils/
│   │   └── weather.py                 # Funkcje do pobierania pogody
│   └── tests/                         # Testy
│       ├── conftest.py
│       ├── test_integration_auth.py
│       ├── test_integration_activities.py
│       ├── test_mocked_db.py
│       └── test_unit_weather.py
│
└── frontend/                          # Kod frontendu (React/TypeScript)
    ├── index.html                     # HTML entry point
    ├── tsconfig.json                  # Konfiguracja TypeScript
    ├── vite.config.ts                 # Konfiguracja Vite
    └── src/
        ├── App.tsx                    # Główny komponent React
        ├── main.tsx                   # React entry point
        └── index.css                  # Globalne style
```

---

## 🔌 API Endpoints

### Authentication (`/api`)

| Metoda | Endpoint | Opis | Body |
|--------|----------|------|------|
| POST | `/api/register` | Rejestracja nowego użytkownika | `{"username": "string", "password": "string"}` |
| POST | `/api/login` | Logowanie użytkownika | `{"username": "string", "password": "string"}` |

**Przykład:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "pass123"}'
```

### Activities (`/activity`)

| Metoda | Endpoint | Opis | Body |
|--------|----------|------|------|
| GET | `/activity` | Pobierz wszystkie aktywności | - |
| POST | `/activity` | Utwórz nową aktywność | `{"username": "string", "name": "string", "description": "string", "city": "string", "planned_date": "YYYY-MM-DD", "planned_time": "HH:MM"}` |
| PUT | `/activity/<id>` | Edytuj aktywność | Jak POST |
| DELETE | `/activity/<id>` | Usuń aktywność | `{"username": "string"}` |
| POST | `/activity/<id>/like` | Polub aktywność | `{"username": "string"}` |
| DELETE | `/activity/<id>/like` | Usuń polubienie | `{"username": "string"}` |

**Przykład dodania aktywności:**
```bash
curl -X POST http://localhost:5000/activity \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "name": "Bieganie",
    "description": "Poranny jogging",
    "city": "Warszawa",
    "planned_date": "2026-03-15",
    "planned_time": "06:30"
  }'
```

---

## 💾 Baza danych

### MongoDB - Struktura kolekcji

#### `users`
```json
{
  "_id": ObjectId,
  "username": "string",
  "password": "string (niezaszyfrowane - NIE dla produkcji!)"
}
```

#### `activities`
```json
{
  "_id": ObjectId,
  "username": "string",
  "name": "string",
  "description": "string",
  "city": "string",
  "planned_date": "YYYY-MM-DD",
  "planned_time": "HH:MM",
  "temperature": "number (°C)",
  "windspeed": "number (km/h)",
  "precipitation": "number (mm)",
  "timestamp": "YYYY-MM-DD HH:MM:SS"
}
```

#### `likes`
```json
{
  "_id": ObjectId,
  "activity_id": "string (ObjectId as string)",
  "username": "string"
}
```

### Połączenie z MongoDB

Edytuj plik `backend/database.py`:
```python
MONGO_URI = "mongodb://localhost:27017/activity_db"
```

---

## 🧪 Testowanie

### Uruchomienie wszystkich testów:

```powershell
cd backend
pytest
```

### Uruchomienie konkretnych testów:

```powershell
# Testy jednostkowe pogody
pytest tests/test_unit_weather.py -v

# Testy integracyjne autoryzacji
pytest tests/test_integration_auth.py -v

# Testy integracyjne aktywności
pytest tests/test_integration_activities.py -v

# Testy z mockowaną bazą
pytest tests/test_mocked_db.py -v
```

### Pokrycie testami:

```powershell
pip install pytest-cov
pytest --cov=. --cov-report=html
# Otwórz htmlcov/index.html
```

---

## 🔧 Dostępne komendy

### Frontend:

```powershell
npm run dev       # Uruchom dev server
npm run build     # Build produkcyjny
npm run preview   # Podgląd buildu
npm run lint      # Sprawdzenie TypeScript
npm run clean     # Wyczyść folder dist
```

### Backend:

```powershell
python app.py     # Uruchom aplikację
pytest            # Uruchom testy
```

---

## ❌ Troubleshooting

### Problem: "Connection refused" do MongoDB

**Rozwiązanie:**
```powershell
# Sprawdź, czy Docker jest uruchomiony
docker ps

# Uruchom MongoDB ponownie
docker-compose up -d

# Lub sprawdź czy MongoDB słucha na porcie
netstat -an | Select-String "27017"
```

### Problem: CORS errors

Jeśli widzisz błędy CORS w konsoli frontendu:
- Upewnij się, że backend jest uruchomiony na `localhost:5000`
- Sprawdź czy `flask_cors.CORS(app)` jest zainicjalizowany w `app.py`

### Problem: Port 5000 już w użyciu

```powershell
# Znaleźć proces na porcie 5000
netstat -ano | findstr "5000"

# Zabić proces (replace PID)
taskkill /PID <PID> /F
```

### Problem: Zła wersja Python

```powershell
# Sprawdź wersję
python --version

# Jeśli masz Python 2, użyj:
python3 --version
python3 -m venv venv
```

### Problem: npm install nie działa

```powershell
# Wyczyść cache npm
npm cache clean --force

# Usuń node_modules i package-lock.json
rm -r node_modules package-lock.json

# Zainstaluj ponownie
npm install
```

---

## 🔐 Uwagi bezpieczeństwa

⚠️ **WAŻNE:** Aktualna implementacja nie jest bezpieczna dla produkcji:

- ❌ Hasła są przechowywane w czystym tekście - użyj `bcrypt` do hashowania
- ❌ Brak JWT tokenów - implementuj autoryzację sessionową
- ❌ Brak walidacji inputów - dodaj `Marshmallow` lub `Pydantic`
- ❌ Brak rate limitingu - dodaj `Flask-Limiter`
- ❌ Brak HTTPS - zawsze używaj SSL/TLS w produkcji

---

## 📚 Dodatkowe zasoby

- [Flask dokumentacja](https://flask.palletsprojects.com/)
- [React dokumentacja](https://react.dev/)
- [MongoDB dokumentacja](https://docs.mongodb.com/)
- [Vite dokumentacja](https://vitejs.dev/)
- [TailwindCSS dokumentacja](https://tailwindcss.com/)

---

## 📧 Kontakt i wsparcie

Jeśli masz problemy, sprawdź:
1. Czy wszystkie dependencje są zainstalowane
2. Czy MongoDB jest uruchomiony
3. Czy porty 5000 i 5173 są dostępne
4. Logi w konsoli backendu i frontendu

---

**Ostatnia aktualizacja:** Marzec 2026
**Wersja:** 1.0.0
