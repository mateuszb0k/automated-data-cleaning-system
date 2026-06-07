import pandas as pd

from src.pipeline.storage_manager import createDataFrame
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

def checkRules(data:pd.DataFrame):
    """
    Validates a dataframe against predefined boundaries and returns a dataFrame with an added bool column is_anomaly
    """
    rules = load_rules()
    data['is_anomaly'] = False
    for FEATURE in FEATURES_TO_CHECK:
        data[f'is_anomaly'] |= (data[f'{FEATURE}'] < rules[f'{FEATURE}']['min']) | (data[f'{FEATURE}'] > rules[f'{FEATURE}']['max'])
    clean_data = data[~data['is_anomaly']]
    quarantine_data = data[data['is_anomaly']]
    return clean_data, quarantine_data
def zScoreDecisionMaking(data :pd.DataFrame):
    '''
    Uses z score to check for anomalies
    '''
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.sort_values(by=['station_id', 'timestamp'], ascending=True, inplace=True)
    rules = load_rules()
    for FEATURE in FEATURES_TO_CHECK:
        if FEATURE == 'rain_mm' or FEATURE == 'wind_direction':
            data[f'{FEATURE}_is_anomaly'] = (data[f'{FEATURE}']<rules[f'{FEATURE}']['min']) | (data[f'{FEATURE}']>rules[f'{FEATURE}']['max'])
        else:
            data[f'{FEATURE}_rolling_mean'] = data.groupby('station_id')[f'{FEATURE}'].transform(lambda x: x.rolling(window = 14,min_periods=1).mean())
            data[f'{FEATURE}_rolling_std'] = data.groupby('station_id')[f'{FEATURE}'].transform(lambda x: x.rolling(window = 14,min_periods=1).std())
            data[f'{FEATURE}_z_score'] = (data[f'{FEATURE}'] - data[f'{FEATURE}_rolling_mean']) / data[f'{FEATURE}_rolling_std']
            data[f'{FEATURE}_is_anomaly'] = (data[f'{FEATURE}_z_score'].abs()>MEAN_MULTIPLE) & (data[f'{FEATURE}_rolling_std'].abs()>0)
    return data


if __name__ == "__main__":
    df = createDataFrame()
    clean_data,quarantine_data = checkRules(df)
    processed_df = zScoreDecisionMaking(clean_data)
    for feature in FEATURES_TO_CHECK:
        feature_anomaly = processed_df[processed_df[f'{feature}_is_anomaly'] == True]
        print(feature_anomaly[['timestamp', 'station_id', f'{feature}']] if feature == 'rain_mm' or feature == 'wind_direction' else feature_anomaly[['timestamp', 'station_id', f'{feature}', f'{feature}_z_score']])