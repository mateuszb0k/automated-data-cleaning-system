import requests
import os
import dotenv
import json
'''
    Creates json files for each weather station data
'''
dotenv.load("../../config/.env")
API_URL = os.getenv("WEATHER_API_URL")
API_KEY = os.getenv("WEATHER_API_TOKEN")
STATIONS = list(requests.get(API_URL+"/weather/stations", headers={"Authorization": API_KEY}).json().values())[0]
LIMIT = 50

if __name__ == "__main__":
    for station in STATIONS:
        os.makedirs(f'../data/bronze/{station}', exist_ok=True)
        weather_data = requests.get(f"{API_URL}/weather/batch?station_id={station}&limit={LIMIT}",headers={"Authorization": API_KEY}).json()

        for single_timestamp in weather_data['records']:
            timestamp_cleaned = single_timestamp["timestamp"].replace(':','_')
            json.dump(single_timestamp, open(f"../data/bronze/{station}/{station}_{timestamp_cleaned}.json", "w"))