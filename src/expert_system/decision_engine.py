import pandas as pd
import os

from src.pipeline.storage_manager import createDataFrame, exportData
from src.pipeline.audit_loger import save_audit_logs

from src.models.baseline_stats import zScoreDecisionMaking
from src.models.imputation_ml import fixAnomalies, cleanData

from src.config.utils import FEATURES_TO_CHECK, load_rules


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

if __name__ == "__main__":

    df = createDataFrame()

    clean_data,quarantine_data = checkRules(df)
   
    processed_df = zScoreDecisionMaking(clean_data)

    fixed_Data, change_logs = fixAnomalies(processed_df)

    cleaned_data = cleanData(fixed_Data)

    exportData(quarantine_data,'../data/quarantine','quarantine_data.json')
    exportData(cleaned_data,'../data/silver','silver_data.json')
    change_logs_df = pd.DataFrame(change_logs)
    save_audit_logs(change_logs_df,'audit_logs.json')
   
            # reparing anomalies data with rolling mean value from last 14 measurments
        # processed_df.loc[processed_df[f'{feature}_is_anomaly']==True,feature] = processed_df[f'{feature}_rolling_mean']
            # print(feature_anomaly[['timestamp', 'station_id', f'{feature}']] if feature == 'rain_mm' or feature == 'wind_direction' else feature_anomaly[['timestamp', 'station_id', f'{feature}', f'{feature}_z_score']])