import pandas as pd

from src.pipeline.storage_manager import createDataFrame
import json

def load_rules():
    """
    Loads the rules from 'config/cleaning_rules.json'.
    """
    json_path = '../../config/cleaning_rules.json'
    with open(json_path, 'r') as f:
        return json.load(f)

def checkRow(row, rules):
    """
    Validates a row against predefined boundaries and returns a dictionary of detected missing or out-of-bounds values.
    """
    wrong_values = {}
    for label, value in row.items():
        if label in rules:
            if pd.isna(value):
                wrong_values[label] = "NaN"
                continue

            if value < rules[label]['min'] or value > rules[label]['max']:
                wrong_values[label] = value

    return None if not wrong_values else wrong_values

if __name__ == "__main__":
    rules = load_rules()
    df = createDataFrame()
    for idx, row in df.iterrows():
        errors = checkRow(row, rules)
        if errors is not None:
            print(row["timestamp"], errors)
