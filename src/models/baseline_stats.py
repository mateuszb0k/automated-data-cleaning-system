import json
import pandas as pd
from src.config.utils import FEATURES_TO_CHECK,MEAN_MULTIPLE, load_rules


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
