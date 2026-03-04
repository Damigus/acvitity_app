import requests
from datetime import datetime

def get_weather_data(city_name, planned_date=None, planned_time=None):
    cities = {
        "Warszawa": {"lat": 52.2297, "lon": 21.0122},
        "Krakow": {"lat": 50.0647, "lon": 19.9450},
        "Gdansk": {"lat": 54.3520, "lon": 18.6466},
        "Poznan": {"lat": 52.4064, "lon": 16.9252}
    }
    coords = cities.get(city_name, cities["Warszawa"])
    
    try:
        if not planned_date or not planned_time:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,wind_speed_10m,precipitation"
            response = requests.get(url, timeout=5)
            data = response.json()
            return {
                "temperature": data['current']['temperature_2m'],
                "windspeed": data['current']['wind_speed_10m'],
                "precipitation": data['current']['precipitation']
            }
        
        # prognoza godzinowa do 14 dni
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&hourly=temperature_2m,windspeed_10m,precipitation&timezone=auto&forecast_days=14"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        hour = planned_time.split(":")[0].zfill(2)
        target = f"{planned_date}T{hour}:00"
        
        if target in data['hourly']['time']:
            idx = data['hourly']['time'].index(target)
            return {
                "temperature": data['hourly']['temperature_2m'][idx],
                "windspeed": data['hourly']['windspeed_10m'][idx],
                "precipitation": data['hourly']['precipitation'][idx]
            }
        return {"temperature": 0, "windspeed": 0, "precipitation": 0}
    except Exception as e:
        print(f"blad pogody {e}")
        return {"temperature": 0, "windspeed": 0, "precipitation": 0}
