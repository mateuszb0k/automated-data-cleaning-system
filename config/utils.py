import json

FEATURES_TO_CHECK=[
    'temperature',
    'humidity',
    'pressure',
    'wind_speed',
    'rain_mm',
    'wind_direction',
]
MEAN_MULTIPLE = 2

def load_rules():
    """
    Loads the rules from 'config/cleaning_rules.json'.
    """
    json_path = '../../config/cleaning_rules.json'
    with open(json_path, 'r') as f:
        return json.load(f)
