import requests
import os
import dotenv
import json
'''
    Creates json files for each weather station data
'''
dotenv.load("config/.env") # If running from main remove "../../"
API_URL = os.getenv("WEATHER_API_URL")
API_KEY = os.getenv("WEATHER_API_TOKEN")
STATIONS = list(requests.get(str(API_URL)+"/weather/stations", headers={"Authorization": API_KEY}).json().values())[0]
LIMIT = 50

def get_weather_data(stations, limit):
    for station in stations:
        os.makedirs(f'src/data/bronze/{station}', exist_ok=True) # If running from main replace "../" with "src"
        weather_data = requests.get(f"{API_URL}/weather/batch?station_id={station}&limit={limit}",headers={"Authorization": API_KEY}).json()

        for single_timestamp in weather_data['records']:
            timestamp_cleaned = single_timestamp["timestamp"].replace(':','_')
            json.dump(single_timestamp, open(f"src/data/bronze/{station}/{station}_{timestamp_cleaned}.json", "w")) # If running from main replace "../" with "src"

if __name__ == "__main__":
    get_weather_data(STATIONS, LIMIT)