# Weather Activity Planner

A simple web application to plan activities based on weather data.

## Features
- User authentication (Login/Register)
- Plan activities in specific cities
- Automatic weather data fetching for planned activities
- Social features: Like and interact with activities

## Tech Stack
- **Frontend:** React, Tailwind CSS, Vite
- **Backend:** Python (Flask), MongoDB
- **Testing:** Pytest with MagicMock

## Getting Started

### Database (Docker)
Run MongoDB using Docker:
```bash
docker run -d --name mongodb -p 27017:27017 mongo
```

### Backend
1. Go to the `backend` directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python app.py` (or `flask run`)

### Frontend
1. Go to the `frontend` directory.
2. Install dependencies: `npm install`
3. Run the dev server: `npm run dev`

## Testing
Run unit tests using:
```bash
cd backend
pytest tests/unit_tests.py
```
