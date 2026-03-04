from pymongo import MongoClient
import os

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
        return client.weather_db
    except Exception as e:
        print(f"blad polaczenia z mongodb {e}")
        return None
