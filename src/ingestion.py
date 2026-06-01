import requests
import os
import dotenv
import json
dotenv.load("../config/.env")
API_URL = os.getenv("WEATHER_API_URL")
API_KEY = os.getenv("WEATHER_API_TOKEN")
STATIONS = list(requests.get(API_URL+"/weather/stations", headers={"Authorization": API_KEY}).json().values())[0]
if __name__ == "__main__":
    for station in STATIONS:
        latest_weather_data = requests.get(API_URL+f"/weather/latest?station_id={station}",headers={"Authorization": API_KEY}).json()
        timestamp_cleaned = latest_weather_data["timestamp"].split('.')[0]
        print(timestamp_cleaned)
        json.dump(latest_weather_data,open(f"../data/bronze/{station}_{timestamp_cleaned}.json","w"))
