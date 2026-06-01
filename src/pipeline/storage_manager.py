from pathlib import Path
import pandas as pd

def createDataFrame():
    """
    Creates a Data Frame from data located in './data/bronze'.
    :return:
    pd.DataFrame: A DataFrame containing the following columns:
            - timestamp
            - station_id
            - temperature
            - humidity
            - pressure
            - wind_speed
            - wind_direction
            - rain_mm
            - cloud_cover
    """
    all_json_files = list(Path('../../data/bronze').rglob('*.json'))
    df = pd.DataFrame()
    for json_file in all_json_files:
        df_row = pd.read_json(str(json_file), typ="series").to_frame().T
        df = pd.concat([df, df_row], ignore_index=True)
    return df