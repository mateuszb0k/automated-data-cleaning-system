import pandas as pd
import numpy as np
from src.config.utils import FEATURES_TO_CHECK



def fixAnomalies(data:pd.DataFrame):
    changes = []
    for feature in FEATURES_TO_CHECK:
       if f'{feature}_is_anomaly' in data.columns and f'{feature}_rolling_mean' in data.columns:
                feature_anomaly = data[data[f'{feature}_is_anomaly'] == True]
                for _,row in feature_anomaly.iterrows():
                    changes.append({
                        'timestamp': row['timestamp'],
                        'station_id':row['station_id'],
                        'feature':feature,
                        'original_value':row[feature],
                        'new_value':row[f'{feature}_rolling_mean'],
                        'action':'Z-Score Imputation'
                    })
                
                data[feature] = np.where(data[f'{feature}_is_anomaly'] == True,
                                                 data[f'{feature}_rolling_mean'],
                                                 data[feature])
    return data,changes          

def cleanData(data:pd.DataFrame):
    columns_to_save = ['timestamp','station_id']+FEATURES_TO_CHECK
    return data[columns_to_save]